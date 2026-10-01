## 3.1 Package Ingress & Outer Dropper Mapping

The outer application wrapper, operating under the package namespace `com.zaika.dropper`, acts as a highly specialized delivery mechanism designed to trick the user into granting critical system permissions. Analysis of the Dalvik bytecode revealed three distinct component classes responsible for ingress and persistence:

1. **InstallReceiver:** This class inherits from `BroadcastReceiver`. It statically registers an intent filter in the manifest for `android.intent.action.PACKAGE_ADDED`. By doing so, the malware effectively wakes up in the background whenever a new application is installed on the victim's device, ensuring continuous execution independent of the main UI thread.
2. **MainActivity:** The primary entry point that is launched when the user clicks the application icon. To evade static analysis engines that parse XML layout files for malicious strings, `MainActivity` completely avoids standard layout inflaters. Instead, it utilizes programmatic UI rendering, dynamically drawing buttons, text fields, and progress bars directly from raw Java code. The rendered UI impersonates a critical Google Play Store dialog, flashing text such as "Update available" and "Downloading...".
3. **SinkholeVpn:** Once the user clicks the "Update" button, the application triggers a system-level Android prompt requesting permission to set up a VPN connection. The label presented to the user is deceptively titled "System Update Sync". If granted, this permission launches the `SinkholeVpn` service, locking the device into the malware's control.

[TABLE_CAPTION] Table 1: Threat Model Invariants Table
| Domain | Mechanism / Artifact | Observation |
| Primary Target | ICICI CREDIT CARD.apk | Banking impersonation lure. |
| Outer Package | com.zaika.dropper | The initial dropper wrapper. |
| Inner Package | com.nesuttor.systemup | The decrypted malicious payload. |
| Persistence | PACKAGE_ADDED | Triggers via InstallReceiver. |
| Evasion Mechanics | Programmatic UI | Bypasses XML scanners and breaks AST. |
| Traffic Interception | SinkholeVpn | Full-device in-memory packet capture. |

## 3.2 TUN Interface Virtual Network Traffic Hijacking

The `SinkholeVpn` class extends the native Android `VpnService`. An in-depth audit of its lifecycle execution, specifically the `onStartCommand()` method, revealed the instantiation of a virtual TUN network interface.

By injecting the global routing command `0.0.0.0/0`, the application forces the Android OS to route all internet traffic directly into the malware's process memory space instead of the regular carrier network. This enables immediate packet interception and positions the dropper as an in-memory Man-In-The-Middle (MITM) proxy.

## 3.3 Control-Flow Flattening Decompiler Bypass & ASM Fallback

While `MainActivity` and `SinkholeVpn` handle the ingress, a background worker class designated `a.c` orchestrates the unpacking of the true payload. Initial attempts to decompile `a.c` using JADX-GUI resulted in a total heuristic failure due to control-flow flattening.

Control-flow flattening is an advanced obfuscation technique where standard linear execution (loops, if/else blocks) is replaced by a massive switch statement enclosed within a single infinite loop. State variables dictate the next block to execute, completely destroying the visual hierarchy of the code and deliberately exhausting decompiler AST thresholds. JADX-GUI aborted analysis with the following verbatim error:

```
Method dump skipped, instruction units count: 874
UnsupportedOperationException: Method not decompiled: a.c.run():void
```

By switching JADX into Fallback mode (enabling "Show inconsistent code" and setting verbosity to DEBUG), the raw Dalvik assembly was exposed. Specifically, analysis isolated a bytecode switch-block identified as State 7, representing the runtime initial startup sequence.

## 3.4 Bitwise XOR Mathematical Key Recovery Matrix

The disassembly showed that the application was pulling fragmented files from an obfuscated subfolder named `res/ChandrasekharaVenkata543/`. Four heavily masked component files were identified via their corresponding Hex IDs in `R.java`.

To decrypt these files, we traced the key tracker variable `r7`. The mathematical derivation proved that the XOR key was dynamically generated relative to the array index loop pointer `r5`. The equation derived from the assembly is:

Key = r5 + 170

Because the decryption loop reads the resource blocks in a strict numerical sequence (File 1 to File 4), the specific XOR key mutates for each file fragment.

[TABLE_CAPTION] Table 2: Bitwise XOR Mathematical Key Recovery Matrix
| Sequence / File Name | Resource Block Index | XOR Key | Hex Value |
| File 1: res_0x7f030001.bin | 0 | 170 | 0xAA |
| File 2: res_0x7f030003.so | 1 | 171 | 0xAB |
| File 3: res_0x7f030002.data | 2 | 172 | 0xAC |
| File 4: res_0x7f030000.dex | 3 | 173 | 0xAD |

## 3.5 Multistage Payload Reassembly

Further analysis of the fallback bytecode revealed output stream writers appending the decrypted output blocks linearly into a single destination file. The logic reads File 1, decrypts it with `0xAA`, appends it to a stream; reads File 2, decrypts with `0xAB`, appends it; and so on. The final unified byte array is flushed to a local file internally named `update_payload.apk`.

```python
import os

def decrypt_payload():
    files_in_sequence = [
        ("res_0x7f030001.bin", 0xAA),
        ("res_0x7f030003.so",  0xAB),
        ("res_0x7f030002",      0xAC),
        ("res_0x7f030000.dex", 0xAD)
    ]
    output_filename = "decrypted_payload.apk"
    with open(output_filename, 'wb') as outfile:
        for file_name, key in files_in_sequence:
            with open(file_name, 'rb') as infile:
                encrypted = infile.read()
            decrypted = bytearray([b ^ key for b in encrypted])
            outfile.write(decrypted)
```

## 3.6 Obfuscated Firebase SDK Telemetry & C2 Schema Mapping

Decompilation of `com.nesuttor.systemup` revealed extensive use of the Google Firebase SDK as the primary C2 backend. Tracing initialization strings inside the class `c1.h` exposed queries for `google_app_id`, `google_api_key`, and `firebase_database_url`.

[TABLE_CAPTION] Table 3: Obfuscated Firebase C2 Configuration Constants
| Asset / Parameter Type | Hex ID | Extracted Plaintext Value |
| Database C2 Endpoint | 0x7f100046 | https://server-1-fac9a-default-rtdb.firebaseio.com |
| Storage Bucket | 0x7f10004b | server-1-fac9a.firebasestorage.app |
| GCP Project ID | 0x7f1000b8 | server-1-fac9a |

## 3.7 Certificate Forensics & Infrastructure IP Resolution

Forensic analysis of the signing certificate (`META-INF/ANDROID.RSA`) exposed a generic, unaltered Android Open Source Project (AOSP) developer signature. The presence of this unaltered testkey confirms the threat actor utilized an automated packer or off-the-shelf compilation toolkit without cleaning build artifacts.

Triangulation of the C2 infrastructure was executed via DNS resolution of the Firebase domain endpoint:

```
nslookup server-1-fac9a-default-rtdb.firebaseio.com
Address: 192.168.157.2#53
IPv4: 35.190.39.113, 34.120.206.254, 34.120.160.131, 35.201.97.85
```

These IP ranges map directly to Google Cloud Platform (GCP) infrastructure. Threat intelligence correlation assesses with high confidence that the attacker is leveraging abused, freely provisioned Google Cloud services to host the campaign, exploiting legitimate infrastructure to bypass basic DNS blocklists.
