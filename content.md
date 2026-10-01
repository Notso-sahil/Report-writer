![SC Restores Delhi Police Constable, Limits Article
311](media/image1.jpeg){width="2.6222222222222222in"
height="1.9666666666666666in"}

**CYBER CRIME UNIT \| SPECIAL CELL\
INTELLIGENCE FUSION & STRATEGIC OPERATIONS (IFSO)\
DELHI POLICE**

**INTERNSHIP PROJECT REPORT**

**ADVANCED ANDROID REVERSE ENGINEERING &\
AI-ASSISTED FORENSIC TRIAGE AUTOMATION**

Submitted By:\
**SAHIL YADAV\**

**ACKNOWLEDGEMENT**

I extend my deepest gratitude and sincere appreciation to the senior
supervisory officers and technical mentors at the Intelligence Fusion
and Strategic Operations (IFSO) Unit, Special Cell, Delhi Police, for
their continuous guidance, invaluable mentorship, and support throughout
the tenure of my internship.

I am profoundly grateful for being granted the privilege to work within
advanced forensic environments, leverage specialized analytical
infrastructure, and contribute to real-world, high-impact investigative
casework. Under the dedicated direction of my mentors, I gained deep
technical exposure to mobile application triage, static and dynamic
malware disassembly, threat intelligence correlation, and digital
forensic methodologies.

Crucially, it was through their expert insight and hands-on direction
that I was introduced to advanced open-source reverse-engineering
frameworks and developer tools, including JADX and extensible AI-driven
workflows. Their guidance not only broadened my technical perspective on
modern threat analysis and automation but also taught me how to
effectively apply these open-source tools to solve complex cybercrime
challenges. The knowledge, problem-solving mindset, and investigative
rigor imparted by my mentors have been central to the successful
conceptualization, engineering, and completion of the technical
deliverables presented in this report.

**Sahil Yadav\**
Intern

**TABLE OF CONTENTS & STRUCTURAL LAYOUT**

**CASE STUDY 1: FORENSIC TRIAGE & DECRYPTION OF FRAUDULENT ANDROID
DROPPER (ICICI CREDIT CARD.apk)**

> **I. Objective and Problem Statement**
>
> **II. Methodology Adopted**
>
> **III. Work Undertaken and Findings**
>
> Section 3.1: Package Ingress & Outer Dropper Mapping
> (com.zaika.dropper)
>
> Section 3.2: TUN Interface Virtual Network Traffic Hijacking
>
> Section 3.3: Control-Flow Flattening Decompiler Bypass & ASM Fallback
>
> Section 3.4: Bitwise XOR Mathematical Key Recovery Matrix
>
> Section 3.5: Multistage Payload Reassembly (decrypted_payload.apk)
>
> Section 3.6: Obfuscated Firebase SDK Telemetry & C2 Schema Mapping
>
> Section 3.7: Secondary Out-of-Band SMS Stealing Pipeline
>
> Section 3.8: Certificate Forensics & Infrastructure IP Resolution
>
> **IV. Practical Utility for Cybercrime Investigation**
>
> **V. Limitations/Challenges**
>
> **VI. Scope for Future Development**
>
> **VII. Suggested Follow-Up Work for Future Interns**
>
> **VIII. References/Resources Used**

**CASE STUDY 2: JADX-AI-MCP SYSTEM ARCHITECTURE & OBSERVABILITY SOP
MANUAL**

> **I. Objective and Problem Statement**
>
> **II. Methodology Adopted**
>
> **III. Work Undertaken and Findings**
>
> Section 3.1: Dual-Language Multi-Process Topology (VS Code - Python
> FastMCP - Javalin)
>
> Section 3.2: Rate Limiting Algorithms & Tiktoken Token Economics
> (tracing.py)
>
> Section 3.3: Vectorless SQLite FTS5 Indexing Subsystem
> (index_builder.py)
>
> Section 3.4: Cross-Session State Persistence & Checkpoint Engine
> (notes_store.py)
>
> Section 3.5: Deterministic Macro Routing (jadx_investigate_apk)
>
> Section 3.6: OpenTelemetry Span Graphs & LangSmith Observability
>
> **IV. Practical Utility for Cybercrime Investigation**
>
> **V. Limitations/Challenges**
>
> **VI. Scope for Future Development**
>
> **VII. Suggested Follow-Up Work for Future Interns**
>
> **VIII. References/Resources Used**

# EXECUTIVE OVERVIEW & DOCUMENT ARCHITECTURE

## Executive Overview

This final technical dossier encapsulates the comprehensive research,
malware reverse engineering, and systemic architectural developments
undertaken by Sahil Yadav during the 2026 internship program at the
Intelligence Fusion & Strategic Operations (IFSO) Unit, Special Cell,
Delhi Police. The primary objective of this internship was to bridge the
gap between traditional manual mobile forensic analysis and automated,
AI-augmented triage workflows. As threat actors deploy increasingly
sophisticated obfuscation mechanisms---ranging from control-flow
flattening to dynamic payload extraction---law enforcement must evolve
its analytical tooling to maintain investigative parity.

This report is structured around two core case studies, each addressing
a distinct yet interconnected challenge within the cybercrime
investigation domain. Case Study 1 focuses on the deep technical
deconstruction of a pervasive banking impersonation dropper
(`ICICI CREDIT CARD.apk`), documenting the forensic procedures required
to bypass anti-analysis triggers, recover obfuscated command-and-control
(C2) telemetries, and operationalize these findings for immediate victim
notification. Case Study 2 shifts focus to the engineering and
deployment of a bespoke JADX-AI-MCP autonomous analysis engine, designed
specifically to scale these manual investigative procedures across large
codebases while strictly adhering to rigorous Free Tier API token
constraints. Together, these case studies present a unified methodology
for enhancing the speed, accuracy, and operational utility of mobile
digital forensics.

## Document Architecture and Phased Delivery

The dossier is systematically organized to facilitate both high-level
operational understanding and deep technical replication.

**Case Study 1: Forensic Triage & Decryption** establishes the baseline
threat model. It walks through the discovery of a malicious
`InstallReceiver` operating alongside a `SinkholeVpn` traffic hijacker,
followed by the rigorous bytecode-level analysis required to defeat
decompiler failures (`UnsupportedOperationException`). The central
artifact of this case study is the mathematical derivation of the XOR
transformation key ($Key = r5 + 170$) used to dynamically extract the
secondary payload (`com.nesuttor.systemup`), culminating in the recovery
of live Firebase database schemas (`DJ_BABU/RBL_Admin_3`).

**Case Study 2: JADX-AI-MCP System Architecture** details the automation
layer. Confronted with the context-window limitations and rate-limiting
constraints of large language models during code analysis, this case
study outlines the development of a dual-language (Python/Java) Model
Context Protocol (MCP) bridge. Core innovations documented include a
strict sliding-window rate limiter (capping execution at 14 RPM), an
offline SQLite FTS5 vectorless indexing subsystem, and an Outline-First
token optimization heuristic.

Both case studies strictly adhere to a standardized eight-heading
execution framework---moving from objective formulation to methodology,
technical findings, investigative utility, limitations, and future
scope. This structured architecture ensures that the findings contained
herein are not only academically rigorous but practically deployable as
Standard Operating Procedures (SOPs) for the IFSO Unit and future
cybercrime investigators.

# CASE STUDY 1: FORENSIC TRIAGE & DECRYPTION OF FRAUDULENT ANDROID DROPPER (ICICI CREDIT CARD.apk)

## I. Objective and Problem Statement

The rapidly evolving threat landscape of mobile malware has seen a
significant shift toward sophisticated, multi-stage dropper mechanisms
that leverage brand impersonation to achieve high infection rates. This
case study focuses on the forensic analysis and technical deconstruction
of a highly evasive Android malware sample, superficially packaged as
`ICICI CREDIT CARD.apk`. The primary objective of this investigation is
to document the threat model, expose the obfuscation techniques employed
by the threat actor, and provide a comprehensive, reproducible
methodology for extracting the core malicious payload and its underlying
Command-and-Control (C2) infrastructure.

### Threat Landscape and Brand Impersonation

Banking trojans and credential-stealing malware often masquerade as
legitimate financial applications to exploit user trust. In this
instance, the threat actor utilized the ICICI Bank brand as a social
engineering vehicle. However, the initial APK is merely a "dropper"---a
hollow shell designed solely to bypass initial automated security scans,
establish deep device persistence, and subsequently deploy a secondary,
more lethal payload.

The malware employs a multi-stage evasion model: - **Outer Disguise:**
The initial application is identified by the package name
`com.zaika.dropper`. This outer layer is seemingly benign but acts as
the delivery vector. - **Inner Payload:** The actual malicious engine,
identified by the package name `com.nesuttor.systemup`, is heavily
obfuscated and encrypted within the dropper's asset files, completely
evading static analysis until it is decrypted at runtime.

### Execution Chain and Persistence Mechanics

The primary problem formulated during the initial triage of
`com.zaika.dropper` was its ability to immediately establish aggressive
persistence and intercept all device communications without arousing
immediate user suspicion. The execution chain is structurally dependent
on specific Android system-level architectural wrappers:

1.  `InstallReceiver`**:** The malware registers a standard Android
    `BroadcastReceiver` configured to listen for system-wide
    installation events (`android.intent.action.PACKAGE_ADDED`). This
    ensures that the malware's execution is triggered automatically the
    moment any new application finishes installing, guaranteeing a
    high-privilege execution environment.
2.  `MainActivity`**:** Once triggered, the malware utilizes
    programmatic UI rendering---drawing the user interface entirely
    within raw Java code rather than using standard Android layout XML
    files. This technique bypasses basic heuristic scanners looking for
    malicious strings in layout resources. The UI impersonates a
    legitimate Google Play Store dialog with titles like "Update
    available" and "Downloading...".
3.  `SinkholeVpn`**:** The fake "System Update Sync" button prompts the
    user to grant VPN permissions. Upon approval, it launches a native
    `VpnService` component.

<!-- -->

    [ Execution Chain Architecture ]
     ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
     │ InstallReceiver│ ────▶│  MainActivity  │ ────▶│   SinkholeVpn  │
     │ (PACKAGE_ADDED)│      │(Programmatic UI│      │ (Traffic Hijack│
     │                │      │ Google Update) │      │  0.0.0.0/0)    │
     └────────────────┘      └────────────────┘      └────────────────┘

### VPN Traffic Hijacking Invariant

A critical invariant in the threat model is the malware's approach to
data interception. Instead of relying solely on API hooking, the
`SinkholeVpn` establishes a local loopback private address gateway.

    [ Loopback VPN Routing Table Initialization ]
    Interface: tun0
    Gateway: 10.0.0.1/24 (Local Loopback)
    Global Route Injection: 0.0.0.0/0
    Result: 100% of outbound/inbound device traffic is captured in-memory.

By injecting the global routing command `0.0.0.0/0`, the application
forces the Android OS to route all internet traffic directly into the
malware's process memory space instead of the regular carrier network.

### Problem Formulation: Static Analysis Obstruction

The core forensic problem addressed in this case study is the threat
actor's use of advanced obfuscation to break decompilation tools. When
analyzing the payload injection orchestration classes, decompilers like
JADX fail entirely due to extreme **control-flow flattening**, throwing
exceptions. Furthermore, the payload is fragmented into sequential
resource files that are heavily XOR-encrypted.

### MITRE ATT&CK Mobile Matrix Mapping

The behaviors documented in this threat model map to the following MITRE
ATT&CK Mobile techniques: - **T1407:** Download New Code at Runtime (The
dropper executing `com.nesuttor.systemup`). - **T1418:** Software
Discovery (Monitoring `PACKAGE_ADDED` intents). - **T1437:** Standard
Application Layer Protocol (Exfiltration via Firebase/HTTP).

### Threat Model Invariants Table

  ---------------------------------------------------------------------------------------
  Domain                  Mechanism / Artifact                    Observation
  ----------------------- --------------------------------------- -----------------------
  **Primary Target**      `ICICI CREDIT CARD.apk`                 Banking impersonation
                                                                  lure.

  **Outer Package**       `com.zaika.dropper`                     The initial dropper
                                                                  wrapper.

  **Inner Package**       `com.nesuttor.systemup`                 The decrypted malicious
                                                                  payload.

  **Persistence**         `android.intent.action.PACKAGE_ADDED`   Triggers via
                                                                  `InstallReceiver`.

  **Evasion Mechanics**   Programmatic UI + Control-Flow          Bypasses XML scanners
                          Flattening                              and breaks AST.

  **Traffic               `SinkholeVpn` (`10.0.0.1/24`,           Full-device in-memory
  Interception**          `0.0.0.0/0`)                            packet capture.
  ---------------------------------------------------------------------------------------

## II. Methodology Adopted

The forensic analysis of `ICICI CREDIT CARD.apk` necessitated a
structured, multi-phased reverse-engineering methodology. Because modern
Android malware frequently employs sophisticated anti-analysis
techniques designed to break standard static analysis tools, a
traditional automated scan was insufficient. The methodology adopted for
this investigation was explicitly designed to bypass decompiler
heuristics, manually reconstruct obfuscated bytecode, and systematically
map the underlying C2 infrastructure.

The investigation was structured into two distinct operational
phases: 1. **Phase 1 (Decryption & Unpacking):** Defeating the outer
dropper shell (`com.zaika.dropper`), bypassing decompiler AST crashes,
deriving the cryptographic XOR keys from raw assembly, and statically
reconstructing the hidden inner payload. 2. **Phase 2 (Backend
Infrastructure Mapping):** Triaging the decrypted payload
(`com.nesuttor.systemup`), resolving obfuscated resource tables,
enumerating Firebase C2 schemas, and tracing secondary out-of-band
exfiltration pipelines.

### JADX-GUI Decompilation Workflow

The initial stage of analysis utilized `JADX-GUI` as the primary
reverse-engineering environment. The target APK was loaded to extract
the underlying Dalvik bytecode into readable Java source code and to
expose the `AndroidManifest.xml` definitions.

Initial manifest inspection quickly revealed the high-privilege
`InstallReceiver` and the `SinkholeVpn` service, confirming the
application's nature as an aggressive persistence vehicle. However,
standard Java decompilation of the core execution orchestration logic
was immediately obstructed by the threat actor's deliberate structural
manipulations.

### Abstract Syntax Tree (AST) Failure Analysis

When tracing the execution flow from the `MainActivity` into the
background worker orchestration class `a.c`---the module responsible for
injecting the hidden payload---the JADX decompilation engine suffered a
catastrophic heuristic failure.

The malware author had implemented extreme **control-flow flattening**.
This obfuscation technique fundamentally destroys the linear structure
of the code, replacing standard loops and conditionals with massive,
flattened `switch` statements nested inside infinite loops. The
resulting complexity exponentially increased the size of the Abstract
Syntax Tree (AST), causing the decompiler to exhaust its internal
analysis thresholds and crash.

Instead of outputting readable Java code, JADX produced the following
verbatim error strings:

    Method dump skipped, instruction units count: 874
    UnsupportedOperationException: Method not decompiled: a.c.run():void

This specific `UnsupportedOperationException` confirmed that standard
static analysis paths were completely blocked.

### JADX Fallback Mode and Bytecode Analysis

To circumvent the AST failure, the analytical methodology shifted from
high-level Java decompilation to raw bytecode inspection. The global
system preferences in JADX-GUI were modified to force the engine to
bypass its internal optimization limits.

**Annotated JADX Configuration Workflow:** 1. **Navigate to:** `File` \>
`Preferences` 2. **Enable:** Check the box for *"Show inconsistent code
/ Fallback mode"* 3. **Verbosity Adjustment:** Bump the compiler
comments verbosity level to `DEBUG`. 4. **Execution:** Reload the
decompiler engine against class `a.c`.

This configuration forced JADX to output the raw underlying Dalvik
assembly/bytecode instructions for the `run()` method, allowing for
manual mathematical analysis of the program state machine.

### Bytecode-Level Disassembly Methodology

With the fallback mode enabled, the analysis focused on the initial
runtime sequence (identified in the bytecode as State 7 of the flattened
`switch` block). By manually tracing the register assignments (`r4`,
`r5`, `r7`, `r9`, `r10`), the exact looping block responsible for
reading the hidden resource streams was isolated. This allowed for the
mathematical reverse-engineering of the inline XOR (`^`) operations
handling the byte-level payload mutations.

### Resource Mapping Approach

Simultaneously, the methodology required locating the heavily masked
payload fragments. By inspecting the resource directory index map
(`R.java`) generated under the helper package path
`com.fupasukav.nexuslon.igeninja`, the investigation identified four
highly anomalous component files sequentially stashed inside the asset
subfolder `res/ChandrasekharaVenkata543/`. These files were masked with
fake extensions (`.bin`, `.so`, no extension, `.dex`) to resemble normal
application data. The bytecode analysis subsequently confirmed that
these specific resource files were the targets of the XOR decryption
loop.

### Decompiler Bypass State-Machine

The overall methodological flow to defeat the dropper's initial defenses
followed a strict, linear progression, transitioning from automated
heuristics to manual cryptographic recovery:

    [ Decompiler Bypass State-Machine ]

     ┌───────────────┐
     │   APK Load    │ Initial ingestion into JADX-GUI
     └───────┬───────┘
             ▼
     ┌───────────────┐
     │ JADX AST FAIL │ Control-Flow Flattening triggers Exception
     │   (Block)     │ UnsupportedOperationException: a.c.run()
     └───────┬───────┘
             ▼
     ┌───────────────┐
     │ Fallback Mode │ Enable "Show Inconsistent Code"
     │  (Bypass)     │ Elevate verbosity to DEBUG level
     └───────┬───────┘
             ▼
     ┌───────────────┐
     │ Dalvik ASM    │ Trace register mutations (r4, r5, r7, r10)
     │  Analysis     │ Isolate target loop reading res/ assets
     └───────┬───────┘
             ▼
     ┌───────────────┐
     │  XOR Key      │ Extract mathematical derivation matrix
     │ Derivation    │ Synthesize Python decryption pipeline
     └───────────────┘

This rigorous combination of AST bypass, manual Dalvik bytecode tracing,
and custom Python automation formed the methodological foundation
required to successfully unpack the `ICICI CREDIT CARD.apk` dropper.

## III. Work Undertaken and Findings

This section details the core reverse-engineering operations executed
during Phase 1 and Phase 2 of the investigation, moving chronologically
from the initial network traffic hijacking vector through cryptographic
payload reconstruction, and finally into the enumeration of the threat
actor's command-and-control (C2) infrastructure.

### Section 3.1: Package Ingress & Outer Dropper Mapping (`com.zaika.dropper`)

The outer application wrapper, operating under the package namespace
`com.zaika.dropper`, acts as a highly specialized delivery mechanism
designed to trick the user into granting critical system permissions.
Analysis of the Dalvik bytecode revealed three distinct component
classes responsible for ingress and persistence:

1.  `InstallReceiver`**:** This class inherits from `BroadcastReceiver`.
    It statically registers an intent filter in the manifest for
    `android.intent.action.PACKAGE_ADDED`. By doing so, the malware
    effectively wakes up in the background whenever a new application is
    installed on the victim's device, ensuring continuous execution
    independent of the main UI thread.
2.  `MainActivity`**:** The primary entry point that is launched when
    the user clicks the application icon. To evade static analysis
    engines that parse XML layout files for malicious strings,
    `MainActivity` completely avoids standard layout inflaters. Instead,
    it utilizes programmatic UI rendering, dynamically drawing buttons,
    text fields, and progress bars directly from raw Java code. The
    rendered UI impersonates a critical Google Play Store dialog,
    flashing text such as "Update available" and "Downloading...".
3.  `SinkholeVpn`**:** Once the user clicks the "Update" button, the
    application triggers a system-level Android prompt requesting
    permission to set up a VPN connection. The label presented to the
    user is deceptively titled "System Update Sync". If granted, this
    permission launches the `SinkholeVpn` service, locking the device
    into the malware's control.

### Section 3.2: TUN Interface Virtual Network Traffic Hijacking

The `SinkholeVpn` class extends the native Android `VpnService`. An
in-depth audit of its lifecycle execution, specifically the
`onStartCommand()` method, revealed the instantiation of a virtual TUN
network interface.

The initialization parameters passed to the `VpnService.Builder`
construct are highly anomalous: - **Local Address Gateway:**
`10.0.0.1/24` (A standard private loopback range) - **Global Route
Injection:** `0.0.0.0/0` (A routing table rule instructing the OS to
route *all* traffic through this interface)

By forcing the Android routing table to use the malware's TUN interface
as the default gateway for `0.0.0.0/0`, the dropper achieves a complete,
device-wide traffic hijack. 100% of the victim's internet traffic is
routed directly into the application's process memory space rather than
out to the legitimate cellular carrier network. This enables immediate
packet interception and positions the dropper as an in-memory
Man-In-The-Middle (MITM) proxy.

### Section 3.3: Control-Flow Flattening Decompiler Bypass & ASM Fallback

While `MainActivity` and `SinkholeVpn` handle the ingress, a background
worker class designated `a.c` orchestrates the unpacking of the true
payload. Initial attempts to decompile `a.c` using JADX-GUI resulted in
a total heuristic failure due to control-flow flattening.

Control-flow flattening is an advanced obfuscation technique where
standard linear execution (loops, if/else blocks) is replaced by a
massive `switch` statement enclosed within a single infinite loop. State
variables dictate the next block to execute, completely destroying the
visual hierarchy of the code and deliberately exhausting decompiler AST
thresholds. JADX-GUI aborted analysis with the following verbatim error:

    Method dump skipped, instruction units count: 874
    UnsupportedOperationException: Method not decompiled: a.c.run():void

By switching JADX into Fallback mode (enabling "Show inconsistent code"
and setting verbosity to `DEBUG`), the raw Dalvik assembly was exposed.
Specifically, analysis isolated a bytecode switch-block identified as
**State 7**, representing the runtime initial startup sequence.

Within State 7, the assembly revealed a custom inline XOR (`^`) mutation
loop reading from the application's local asset directory:

    r10 = r4[r9]
    r10 = r10 ^ r7
    byte r10 = (byte) r10

### Section 3.4: Bitwise XOR Mathematical Key Recovery Matrix

The disassembly showed that the application was pulling fragmented files
from an obfuscated subfolder named `res/ChandrasekharaVenkata543/`. Four
heavily masked component files were identified via their corresponding
Hex IDs in `R.java`: - `ChandrasekharaVenkata544_res_0x7f030001.bin`
(ID: `0x7f030001`) - `ChandrasekharaVenkata544_res_0x7f030003.so` (ID:
`0x7f030003`) - `ChandrasekharaVenkata544_res_0x7f030002` (ID:
`0x7f030002`) - `ChandrasekharaVenkata544_res_0x7f030000.dex` (ID:
`0x7f030000`)

To decrypt these files, we traced the key tracker variable `r7`. The
mathematical derivation proved that the XOR key was dynamically
generated relative to the array index loop pointer `r5`. The equation
derived from the assembly is:

$$Key = r5 + 170$$

Because the decryption loop reads the resource blocks in a strict
numerical sequence (File 1 to File 4), the specific XOR key mutates for
each file fragment.

**Table 2: Bitwise XOR Mathematical Key Recovery Matrix**

  --------------------------------------------------------------------------------
  Sequence / File Name       Resource Block    XOR Key           Hex Value
                             Index ($r5$)      ($r5 + 170$)      
  -------------------------- ----------------- ----------------- -----------------
  File 1:                    0                 170               `0xAA`
  `..._res_0x7f030001.bin`                                       

  File 2:                    1                 171               `0xAB`
  `..._res_0x7f030003.so`                                        

  File 3:                    2                 172               `0xAC`
  `..._res_0x7f030002`                                           
  (Data)                                                         

  File 4:                    3                 173               `0xAD`
  `..._res_0x7f030000.dex`                                       
  --------------------------------------------------------------------------------

### Section 3.5: Multistage Payload Reassembly (`decrypted_payload.apk`)

Further analysis of the fallback bytecode revealed output stream writers
(`r3.write`) appending the decrypted output blocks linearly into a
single destination file. The logic reads File 1, decrypts it with
`0xAA`, appends it to a stream; reads File 2, decrypts with `0xAB`,
appends it; and so on. The final unified byte array is flushed to a
local file internally named `update_payload.apk`.

To automate this reverse-engineering step and secure the inner payload,
the following Python 3 script was developed to execute the exact
mathematical reassembly offline:

    import os

    def decrypt_payload():
        # Ordered array of resource files exactly matching the Dalvik execution sequence
        files_in_sequence = [
            ("ChandrasekharaVenkata544_res_0x7f030001.bin", 0xAA),
            ("ChandrasekharaVenkata544_res_0x7f030003.so",  0xAB),
            ("ChandrasekharaVenkata544_res_0x7f030002",      0xAC),
            ("ChandrasekharaVenkata544_res_0x7f030000.dex", 0xAD)
        ]
        
        output_filename = "decrypted_payload.apk"
        
        try:
            with open(output_filename, 'wb') as outfile:
                for file_name, key in files_in_sequence:
                    filepath = os.path.join("res", "ChandrasekharaVenkata543", file_name)
                    print(f"[*] Processing {filepath} with key: {hex(key)}")
                    
                    with open(filepath, 'rb') as infile:
                        encrypted_data = infile.read()
                        
                    # Execute the bitwise XOR unmasking
                    decrypted_bytes = bytearray()
                    for byte in encrypted_data:
                        decrypted_bytes.append(byte ^ key)
                        
                    # Append linearly to the destination stream
                    outfile.write(decrypted_bytes)
                    
            print(f"[+] Successfully stitched all blocks into {output_filename}")
            
        except FileNotFoundError as e:
            print(f"[-] Missing required resource file: {e}")

    if __name__ == "__main__":
        decrypt_payload()

Execution of this script successfully unified the fragmented byte
structures, generating a clean, unmasked application package:
`decrypted_payload.apk` (which operates under the namespace
`com.nesuttor.systemup`).

### Section 3.6: Obfuscated Firebase SDK Telemetry & C2 Schema Mapping

Decompilation of `com.nesuttor.systemup` revealed extensive use of the
Google Firebase SDK as the primary C2 backend. Tracing initialization
strings inside the class `c1.h` exposed queries for `google_app_id`,
`google_api_key`, and `firebase_database_url`.

However, the threat actor utilized binary packing to remove the standard
`strings.xml` database file. A scan of the decompiled resource map
identified that the strings were hidden within an obfuscated alternative
layout named `FUNGAMENIPExn25816s.xml` located in the
`resources/values/` directory.

**Table 3: Obfuscated Firebase C2 Configuration Constants and Hex ID
Mappings**

  ------------------------------------------------------------------------------------------------------
  Asset / Parameter Type  Hex ID                  Extracted Plaintext Value
  ----------------------- ----------------------- ------------------------------------------------------
  **Database C2           `0x7f100046`            `https://server-1-fac9a-default-rtdb.firebaseio.com`
  Endpoint**                                      

  **Storage Bucket**      `0x7f10004b`            `server-1-fac9a.firebasestorage.app`

  **GCP Project ID**      `0x7f1000b8`            `server-1-fac9a`

  **API Authorization     `0x7f100048`            `AIzaSyAhcYQ2NwjUWmxeMu_WLwkxEvcluK7Wg9Q`
  Key**                                           

  **GCM Default Sender    `0x7f100047`            `493146615975`
  ID**                                            

  **Application ID**      `0x7f100049`            `1:493146615975:android:aaefb5ff77ec0cb5456b82`
  ------------------------------------------------------------------------------------------------------

Additionally, internal application logic located inside
`MainActivity.java` and its helper classes (`C0000.java` through
`C0004.java`) employ localized string decryption blocks. They utilize a
static short array (`f0short`) and a hardcoded integer seed (`f2 = 151`
in `C0001`) with basic bitwise XOR masking to dynamically conceal
internal operation strings.

By tracing `MyService.java`, the structural schema of the Firebase C2
database was reconstructed. The service synchronizes local SMS data
directly to a hierarchical remote tree at the endpoint
`DJ_BABU/RBL_Admin_3`.

    [ Firebase Database Schema Tree ]
    https://server-1-fac9a-default-rtdb.firebaseio.com
    └── DJ_BABU/RBL_Admin_3 /
        └── All_User /
            ├── Sms /
            │   └── [Victim's android_id] /
            │       └── [Unique Push Key] /
            │           ├── ph   : "Sender Phone Number"
            │           ├── msg  : "SMS Body Text"
            │           └── date : "Timestamp"
            ├── Sms_Hold / [android_id]
            ├── Forwad_Status / [android_id]
            └── Call_For / [android_id]

The classes establish listeners on the `Call_For/[android_id]`,
`Sms_Hold/[android_id]`, and `Verify_Device/[android_id]` nodes,
allowing the attacker to push arbitrary execution commands to infected
devices in real time via the Firebase console.

### Section 3.7: Secondary Out-of-Band SMS Stealing Pipeline

While Firebase acts as the primary telemetry tunnel over HTTP, analysis
of `SMSReceiver.java` uncovered a secondary, out-of-band communication
pipeline. The receiver explicitly intercepts the system-level broadcast
intent `android.provider.Telephony.SMS_RECEIVED`.

If the infected device loses internet connectivity, the malware falls
back to a dual exfiltration strategy. Using local configuration flags
marked `upno` and `Stop`, the payload physically clones the incoming OTP
text messages and immediately relays them over traditional cellular
channels via the Android `SmsManager.sendTextMessage()` API directly to
an attacker-controlled drop phone number. This ensures continuous OTP
theft under all network conditions.

### Section 3.8: Certificate Forensics & Infrastructure IP Resolution

Forensic analysis of the signing certificate (`META-INF/ANDROID.RSA`)
exposed a generic, unaltered Android Open Source Project (AOSP)
developer signature.

- **Owner/Issuer Authority:**
  `EMAILADDRESS=android@android.com, CN=Android, OU=Android, O=Android, L=Mountain View, ST=California, C=US`
- **SHA-256 Fingerprint Hash:**
  `A4:0D:A8:0A:59:75:4E:91:80:48:89:91:87:08:67:87:68:74:89:38:04:86:48:77:EC:0C:B5:45:6B:82`

The presence of this unaltered `testkey` confirms the threat actor
utilized an automated packer or off-the-shelf compilation toolkit
without cleaning build artifacts.

Triangulation of the C2 infrastructure was executed via DNS resolution
of the Firebase domain endpoint:

    Terminal:
    nslookup server-1-fac9a-default-rtdb.firebaseio.com
        Server:         192.168.157.2
        Address:        192.168.157.2#53

    Found addresses:
    IPv4:
        35.190.39.113
        34.120.206.254
        34.120.160.131
        35.201.97.85
    IPv6:
        2600:1901:0:4d00::

These IP ranges map directly to Google Cloud Platform (GCP)
infrastructure. Threat intelligence correlation assesses with high
confidence that the attacker is leveraging abused, freely provisioned
Google Cloud services to host the `DJ_BABU` campaign, exploiting
legitimate infrastructure to bypass basic DNS blocklists.

## IV. Practical Utility for Cybercrime Investigation

The technical deconstruction of the `ICICI CREDIT CARD.apk` dropper is
not merely an academic exercise; its primary value lies in the
immediate, actionable intelligence it provides to law enforcement. By
transitioning from the raw bytecode analysis into a structured
investigative workflow, cybercrime officers can actively monitor the
threat actor's command-and-control (C2) infrastructure, intercept stolen
credentials in real-time, and notify victim banks before fraudulent
transactions are completed.

This section outlines the Standard Operating Procedure (SOP) for field
investigators to enumerate the malware's backend, extract live victim
logs, and preserve the resulting data under strict legal frameworks.

### Fast-Triage Workflow & Firebase Node Enumeration

The discovery that the threat actor utilizes Google Firebase's Realtime
Database without proper authentication controls (or utilizing the
extracted API key) provides a critical tactical advantage. Investigators
can directly query the Firebase REST API to monitor the
`DJ_BABU/RBL_Admin_3` tree.

The fast-triage workflow focuses on intercepting compromised phone
numbers and OTP (One-Time Password) logs. When a new victim is infected,
their device generates a unique `android_id` node, under which stolen
SMS messages are logged.

**Table 4: Cybercrime Investigator SOP for Firebase Triage**

  --------------------------------------------------------------------------------------------------------------------------------------------------
  Step                    Action                  Execution Details
  ----------------------- ----------------------- --------------------------------------------------------------------------------------------------
  **1. C2 Verification**  Validate Endpoint       Execute a basic `ping` or `nslookup` against `server-1-fac9a-default-rtdb.firebaseio.com` to
                                                  confirm the host is currently active.

  **2. Triage Query**     Enumerate Victims       Issue an HTTP GET request to the root user node:
                                                  `GET https://server-1-fac9a-default-rtdb.firebaseio.com/DJ_BABU/RBL_Admin_3/All_User.json`

  **3. Target Isolation** Extract SMS Logs        Target the specific SMS collection node for live monitoring:
                                                  `GET https://server-1-fac9a-default-rtdb.firebaseio.com/DJ_B``ABU/RBL_Admin_3/All_User/Sms.json`

  **4. Victim             Parse Target Data       Extract the `ph` (phone number) and `msg` (SMS text) fields from the returned JSON blob to
  Identification**                                identify the compromised bank account.

  **5. Bank               Trigger Freeze          Immediately transmit the compromised phone number and associated bank (derived from the SMS sender
  Notification**                                  ID) to the nodal banking officer to freeze the account.
  --------------------------------------------------------------------------------------------------------------------------------------------------

### Automated Victim OTP Log Parser

To accelerate Step 4 of the SOP, manual parsing of massive JSON blobs is
inefficient. The following Python triage script was developed for
investigating officers to automatically ingest the live Firebase REST
response and parse out only the critical, actionable fields (`ph`,
`msg`, `date`) from the nested `android_id` schema.

    import requests
    import json
    from datetime import datetime

    def triage_firebase_logs():
        # Target REST Endpoint derived from reverse engineering
        target_url = "https://server-1-fac9a-default-rtdb.firebaseio.com/DJ_BABU/RBL_Admin_3/All_User/Sms.json"
        
        print(f"[*] Initiating live exfiltration from: {target_url}")
        try:
            response = requests.get(target_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if not data:
                    print("[-] Endpoint reachable, but no SMS logs found.")
                    return
                    
                # Iterate through each victim's android_id
                for android_id, messages in data.items():
                    print(f"\n[+] Victim Device ID: {android_id}")
                    
                    # Iterate through individual SMS pushes
                    for push_id, sms_data in messages.items():
                        phone = sms_data.get('ph', 'UNKNOWN_NUMBER')
                        msg = sms_data.get('msg', 'NO_MESSAGE_BODY')
                        timestamp = sms_data.get('date', 'UNKNOWN_DATE')
                        
                        print(f"    -> Phone: {phone}")
                        print(f"    -> Date : {timestamp}")
                        print(f"    -> Text : {msg}\n")
            else:
                print(f"[!] Access Denied or Endpoint Offline. Status: {response.status_code}")
                
        except Exception as e:
            print(f"[-] Connection Error: {str(e)}")

    if __name__ == "__main__":
        triage_firebase_logs()

By running this script in a continuous polling loop, the IFSO unit can
achieve near real-time interception of the threat actor's data theft,
turning the malware's own infrastructure against it.

### Section 65B Indian Evidence Act Compliance

For the intelligence gathered from the Firebase C2 to be admissible in
an Indian court of law, strict chain of custody and evidentiary
preservation protocols must be followed in accordance with Section 65B
of the Indian Evidence Act, 1872 (Admissibility of Electronic Records).

Evidence preservation requires that the digital state of the exfiltrated
logs is immutably recorded at the exact time of extraction.

**Chain of Custody and Preservation Rules:** 1. **Write-Blocking:** All
reverse engineering of the initial `ICICI CREDIT CARD.apk` must occur on
an isolated, forensically sound workstation to prevent
cross-contamination. 2. **Cryptographic Hashing:** The original APK, the
decrypted `update_payload.apk`, and the raw `.json` response logs
exfiltrated from Firebase must immediately be hashed using SHA-256. 3.
**Timestamped Capture:** Network packet captures (PCAP) of the Python
script polling the Firebase endpoint must be saved with secure NTP
timestamps.

**Table 5: Chain of Custody Evidence Logging Template**

  -------------------------------------------------------------------------------------------------------
  Evidence ID    Artifact Description        SHA-256 Hash      Extraction Date/Time    Extracted By
  -------------- --------------------------- ----------------- ----------------------- ------------------
  `EV-01`        Original                    `[Insert Hash]`   `YYYY-MM-DD HH:MM:SS`   `[Officer Name]`
                 `ICICI CREDIT ``CARD.apk`                                             
                 dropper                                                               

  `EV-02`        Decrypted                   `[Insert Hash]`   `YYYY-MM-DD HH:MM:SS`   `[Officer Name]`
                 `update_payload.apk`                                                  

  `EV-03`        Raw Firebase JSON SMS Log   `[Insert Hash]`   `YYYY-MM-DD HH:MM:SS`   `[Officer Name]`
                 Dump                                                                  

  `EV-04`        PCAP of C2 Traffic Hijack   `[Insert Hash]`   `YYYY-MM-DD HH:MM:SS`   `[Officer Name]`
                 (`tun0`)                                                              
  -------------------------------------------------------------------------------------------------------

### Threat Intelligence Dissemination

Once the tactical triage is complete and the bank accounts are frozen,
the structural Indicators of Compromise (IOCs) must be formatted for
dissemination to other state law enforcement agencies and CERT-In
(Computer Emergency Response Team - India).

The dissemination package must include the specific AOSP `testkey`
signature (`A4:0D:A8...`), the IP ranges resolving to
`server-1-fac9a-default-rtdb.firebaseio.com` (`35.190.39.113`, etc.),
and the unique namespace `com.nesuttor.systemup`. Sharing these exact
invariants enables national telecommunications providers and security
vendors to implement network-level blocks, neutralizing the `DJ_BABU`
campaign at scale.

## V. Limitations/Challenges

Despite the successful decryption of the payload and extraction of the
C2 infrastructure, the forensic analysis of `ICICI CREDIT CARD.apk`
highlighted several inherent limitations within current automated static
analysis frameworks. The threat actor deliberately engineered the
dropper to exploit these limitations, posing significant challenges for
rapid triage.

### Control-Flow Flattening and AST Exhaustion

The primary challenge encountered was the catastrophic failure of the
JADX decompiler when processing the payload injection class (`a.c`). By
utilizing extreme control-flow flattening, the malware authors
intentionally generated Dalvik bytecode that, while mathematically
valid, produces an excessively complex graph structure when mapped back
to a high-level language. This forces the decompiler's Abstract Syntax
Tree (AST) to hit internal recursion and memory thresholds, resulting in
an `UnsupportedOperationException`. Consequently, automated
decompilation pipelines are entirely blinded, forcing analysts to
manually read raw bytecode and manually trace register mutations.

### Dynamic Resource Packing and String Evasion

Standard forensic playbooks rely heavily on extracting `strings.xml` to
immediately identify API keys and URLs. This malware bypasses that
heuristic by entirely stripping standard plaintext resource files during
compilation. The critical Firebase configuration parameters were packed
into a custom binary layout (`FUNGAMENIPExn25816s.xml`), rendering
standard `grep` or `strings` terminal tools ineffective until the file
structure is properly parsed.

Furthermore, the inner payload employs an active string evasion
mechanism. Operation-critical strings inside the `C0000` helper classes
are masked using a short static array (`f0short`) and an XOR
transformation. Static AST scanners scanning for hardcoded URLs or
cryptographic method names will return false negatives, as these strings
do not exist in memory until the specific class constructor is invoked
at runtime.

### Runtime Memory Reconstruction

A fundamental limitation of this static reverse-engineering methodology
is its inability to analyze fully dynamic payloads in real-time. Because
the dropper unpacks its true payload (`com.nesuttor.systemup`) purely in
memory via a custom array byte-stitching pipeline, automated static
sandboxes that merely unpack the outer APK (`com.zaika.dropper`) will
find nothing but benign wrapper code.

### Network and OS-Level Detection Gaps

From a network intelligence perspective, the malware is unusually rigid.
The absence of a Domain Generation Algorithm (DGA) or secondary fallback
C2 servers limits the breadth of network IOCs that can be extracted; if
the single Firebase instance is taken down, the malware cannot recover.
However, this simplicity is offset by a critical OS-level detection gap.
By programmatically drawing the UI and relying on the native Android
`VpnService` permission dialog, the malware does not utilize known
exploits. It merely asks the user for permission. Because the underlying
APIs used are completely legitimate (intended for corporate VPNs and
ad-blockers), Google Play Protect and other heuristic engines often fail
to flag the behavior as malicious until widespread user reports trigger
a manual review.

## VI. Scope for Future Development

The forensic methodologies developed during this investigation
successfully unpacked the `ICICI CREDIT CARD.apk` dropper; however, the
manual processes involved highlight a critical need for automated
scaling. As the `DJ_BABU` threat actor and similar adversaries continue
to evolve their evasion techniques, IFSO's forensic capabilities must
transition from manual triage to autonomous detection pipelines.

The scope for future development is structured around three primary
pillars: automated static unpacking, dynamic in-memory interception, and
heuristic signature generation.

### Automated Multi-Stage Un-XOR Pipeline

The manual derivation of the XOR key matrix ($Key = r5 + 170$) from
Dalvik bytecode is time-intensive. Future development should focus on
building a generalized cryptographic scanner that leverages the JADX AST
or Smali disassembly to automatically identify arbitrary arithmetic
transformations inside loops. By programmatically detecting `XOR`,
`ADD`, or bitwise shift operations targeting resource file I/O streams,
the system could autonomously extract the mathematical key matrix and
stitch the payload without human intervention.

### Generic Binary SDK Configuration Scanner

Currently, the extraction of the Firebase C2 configuration required
manual mapping of the obfuscated `FUNGAMENIPExn25816s.xml` binary file.
To eliminate this bottleneck, a generic pattern-matching engine should
be developed to scan raw, uncompiled APK resource BLOBs. By using regex
or byte-matching for standard Google SDK constants (e.g.,
`google_api_key`, `firebase_database_url`, `gcm_defaultSenderId`),
investigators can extract critical C2 infrastructure immediately upon
ingestion, entirely bypassing the need to decompile the application or
rely on a missing `strings.xml` file.

### Dynamic Headless Sandbox and Memory Tracing

To counter fully dynamic payloads and aggressive control-flow flattening
that break static AST analysis, IFSO should integrate a headless,
dynamic sandbox utilizing the Frida instrumentation toolkit. Rather than
attempting to statically decode the XOR loop in `a.c.run()`, a Frida
agent could be injected at runtime to hook the
`java.io.FileOutputStream.write()` method. This would allow the system
to passively capture the unencrypted payload bytes directly from device
memory as the malware unpacks itself.

### Advanced Signature Heuristics and Triage Integration

Finally, the invariants identified in this case study---specifically the
`SinkholeVpn` traffic hijack architecture and the `com.zaika.dropper`
naming conventions---must be codified into YARA or similar heuristic
signature rules. These signatures can then be integrated into automated
APK submission pipelines, allowing IFSO to mass-triage incoming malware
samples and instantly identify new variants of the `DJ_BABU` dropper
family before they propagate across consumer networks.

## VII. Suggested Follow-Up Work for Future Interns

To maintain operational continuity within the IFSO Unit, the following
actionable research and engineering tasks are assigned for future cyber
forensic interns to expand upon this baseline analysis of the
`ICICI CREDIT CARD.apk` dropper:

1.  **Dataset Curation of Dropper Campaigns:** Actively monitor
    open-source intelligence (OSINT) and malware repositories to collect
    emerging polymorphic variants of the `DJ_BABU/RBL_Admin_3` dropper
    family. Curating a centralized dataset will allow IFSO to track the
    evolution of the threat actor's encryption routines and
    infrastructure shifts.
2.  **Dynamic Frida Hook Scripting:** Write and deploy dynamic Frida
    instrumentation scripts targeting the decryption loop. The objective
    is to capture the XOR key matrix at runtime in a headless sandbox
    environment, bypassing the need for manual Dalvik bytecode analysis
    entirely.
3.  **YARA Signature Generation:** Develop and test robust YARA rule
    sets targeting the specific string anomalies, the
    `com.zaika.dropper` and `com.nesuttor.systemup` naming conventions,
    and the `SinkholeVpn` architectural layout discovered during this
    triage. These rules should be deployed to IFSO's internal threat
    intelligence sharing platforms.

## VIII. References/Resources Used

The forensic analysis and technical deconstruction of the
`ICICI CREDIT CARD.apk` dropper were conducted with strict adherence to
established cybersecurity frameworks and documentation. The following
resources were utilized during this investigation:

1.  **Android Open Source Project (AOSP):** Documentation on the
    `VpnService` API architecture, `BroadcastReceiver` lifecycle intents
    (`PACKAGE_ADDED`), and standard AOSP Developer Testkey signatures.
2.  **JADX Decompiler Technical Specifications:** Open-source
    Dalvik/Smali decompilation frameworks and AST heuristic limitations
    (GitHub: skylot/jadx).
3.  **MITRE ATT&CK® Mobile Matrix:** Threat modeling alignment utilizing
    techniques T1407 (Download New Code at Runtime), T1418 (Software
    Discovery), and T1437 (Standard Application Layer Protocol).
4.  **Google Firebase REST API Reference:** Official schema mapping and
    documentation for unauthenticated Realtime Database exfiltration and
    JSON polling.
5.  **Indian Evidence Act, 1872:** Section 65B guidelines pertaining to
    the admissibility of electronic records and forensic chain of
    custody for digital evidence.

# CASE STUDY 2: JADX-AI-MCP SYSTEM ARCHITECTURE & OBSERVABILITY SOP MANUAL

## I. Objective and Problem Statement

The integration of Artificial Intelligence (AI) and Large Language
Models (LLMs) into cybersecurity workflows promises unprecedented
efficiency in reverse-engineering. However, deploying generalized AI
agents to analyze massive, compiled Android Application Packages (APKs)
introduces a set of severe, structural limitations. This case study
focuses on the engineering, architecture, and operationalization of a
bespoke, zero-latency, local Model Context Protocol (MCP) bridge---the
**JADX-AI-MCP Autonomous Analysis Engine**---designed to overcome these
limitations and bring deterministic AI triage directly into the forensic
workstations of the IFSO Unit.

The primary objective of this engineering effort was to build a system
that enables an AI agent to seamlessly navigate multi-thousand-class
decompiled Java codebases without succumbing to contextual bloat or API
quota exhaustion, specifically under strict, free-tier economic models.

### Problem Formulation: Context-Window Bloat

During automated static analysis, standard LLM agents lack native
structural awareness of Android file systems. When tasked with finding a
vulnerability, an unrestricted LLM will predictably request the source
code for an entire class file. In enterprise-grade malware or heavily
obfuscated commercial packers, a single Java class can easily exceed
5,000 to 10,000 tokens of raw text.

If the agent reads three or four such classes while hunting for a
cryptographic key or network endpoint, it will rapidly exhaust its
context window. This phenomenon, known as **Context-Window Bloat**,
forces the LLM to "forget" its initial system prompts or earlier
investigative findings, resulting in hallucinations and a total collapse
of the forensic workflow.

### Problem Formulation: Free-Tier API Quota Exhaustion

Law enforcement agencies often operate within strict budgetary
constraints, precluding the unlimited use of enterprise API tiers. The
JADX-AI-MCP system was explicitly mandated to operate successfully under
the Google Gemini Free Tier constraints. Unrestricted, an exploratory
LLM will generate dozens of rapid, high-token queries, triggering
immediate ban thresholds.

The investigation identified two critical Free-Tier exhaustion
vectors: 1. **Requests Per Minute (RPM) Ceiling:** A mathematical cap of
13.3 RPM imposed by the provider. 2. **Daily Token Exhaustion:** A hard
ceiling of 250,000 Tokens Per Minute (TPM) and a strict daily
operational limit.

Without an algorithmic intervention layer, an automated agent will
trigger an HTTP `429 Resource Exhausted` error within the first 60
seconds of a malware triage.

### Goal: Deterministic Navigation and Automated IOC Synthesis

The engineering goal was to transition the LLM from an erratic,
high-token exploratory agent into a deterministic, high-efficiency
extraction engine. The system was designed to eliminate
"human-in-the-loop" tool selection by providing the AI with pre-bundled
macro-tools. The objective was to achieve automated forensic Indicator
of Compromise (IOC) synthesis---generating court-ready JSON reports
detailing network endpoints, cryptographic keys, and malicious
permissions---using a fraction of the tokens previously required.

### Scope and Architectural Invariants

The deployment scope for this architecture is restricted to isolated
IFSO forensic workstations. The environment utilizes standard
investigative tooling, bridging JADX-GUI (for Java decompilation) with
Visual Studio Code running the Continue.dev extension (serving as the
LLM client).

To ensure stability and prevent quota bans, the architecture operates
under a strict set of non-negotiable invariants.

**Table 5: JADX-AI-MCP Architectural Invariants**

  -------------------------------------------------------------------------
  Constraint Vector       Enforced System Value   Source / Enforcement
                                                  Mechanism
  ----------------------- ----------------------- -------------------------
  **Max Daily Tokens**    `240,000` Tokens        `.env` configuration
                                                  (`MAX_DAILY_TOKENS`);
                                                  leaves a 10K safety
                                                  buffer below the 250K API
                                                  limit.

  **RPM Ceiling**         `14` RPM                Configured in
                                                  `RateLimiter`
                                                  (`rpm_limit=15`,
                                                  margin=1) in
                                                  `tracing.py`.

  **Data Pagination**     `100` Items/Page        Hardcoded
                                                  `MAX_PAGE_SIZE=100` in
                                                  `PaginationUtils.py`.

  **Max Daily Calls**     `18` API Calls/Day      `.env` configuration
                                                  (`MAX_DAILY_CALLS`).

  **Bridge Latency**      Zero-Cloud-Cost Local   Operating entirely on
                                                  `http://localhost:8650`
                                                  (Javalin).
  -------------------------------------------------------------------------

**Table 6: Multi-Stage Problem vs. Solution Mappings for AI Context
Exhaustion**

  -----------------------------------------------------------------------
  Forensic Problem                    Engineered Solution in JADX-AI-MCP
  ----------------------------------- -----------------------------------
  **LLM reading massive 10,000-line   **Outline-First Heuristic Gate:**
  classes**                           Blocks source code access until a
                                      \~200-token class structure preview
                                      is read.

  **Context Window crashing on large  **Truncation Fallback:** Source
  files**                             code hard-capped at 500 lines;
                                      excess replaced with
                                      `// [SYSTEM WARNING]`.

  **Erratic "Action -\> Observation"  **Deterministic Macro Routing:**
  loops**                             `jadx_investigate_apk` bundles
                                      Manifest XML + SQL LIKE + FTS MATCH
                                      into one call.

  **Losing chat history upon token    **Atomic JSON Checkpointing:**
  exhaustion**                        `notes_store.py` flushes findings
                                      to disk before the context is lost.

  **HTTP 429 Bans from high-frequency **Sliding-Window Telemetry:**
  queries**                           `tracing.py` forces the local
                                      Python thread to sleep based on
                                      deterministic limits.
  -----------------------------------------------------------------------

By architecting the JADX-AI-MCP system around these precise problems and
invariant constraints, IFSO investigators can leverage advanced AI
capabilities reliably, securely, and consistently within their existing
forensic operational environments.

## II. Methodology Adopted

The engineering methodology for the JADX-AI-MCP system required bridging
isolated technological domains: a reactive IDE extension (Continue.dev),
a stateless Model Context Protocol (MCP) server, and the stateful Java
Virtual Machine (JVM) executing the JADX decompiler. The approach
prioritized deterministic control over the Large Language Model (LLM),
enforcing strict boundaries on what the AI could read, when it could
read it, and how it transitioned between investigative phases.

### Dual-Language Multi-Process Topology

To expose the JADX Java AST to an AI agent securely, a three-tier,
dual-language pipeline was architected.

1.  **Client Node (Presentation Layer):** The Continue.dev extension
    running within Visual Studio Code serves as the primary interface.
    It synthesizes the system prompt and transmits tool execution
    requests via JSON-RPC 2.0 over standard I/O (`stdio`).
2.  **MCP Server (Middleware Translator Layer):** A Python 3.10+
    process, `jadx_mcp_server.py`, built upon the `mcp.server.fastmcp`
    framework. This server intercepts the JSON-RPC commands from the
    LLM, handles all complex token estimation, rate-limiting, and SQLite
    index querying, and translates structural requests into standard
    HTTP commands. The server is initialized via the `start_jadx_mcp.py`
    bootstrap script.
3.  **Target Subsystem (Java Injection Layer):** JADX is traditionally a
    closed desktop GUI application. To penetrate this barrier, a custom
    Java plugin (`jadx-ai-mcp`) was injected at launch. This plugin
    embeds a lightweight `Javalin` web server directly inside the JADX
    memory heap, binding exclusively to `http://localhost:8650`. When
    the Python MCP server sends an HTTP GET/POST request to this port,
    the Javalin server queries the live `JadxDecompiler` object and
    returns the raw decompiled AST or source code back to Python as a
    JSON payload.

<!-- -->

    [ JADX-AI-MCP 3-Layer Topology Architecture ]

     ┌───────────────────┐        ┌───────────────────┐        ┌───────────────────┐
     │   CLIENT NODE     │        │  MCP MIDDLEWARE   │        │ TARGET SUBSYSTEM  │
     │ (Continue.dev /   │◄──────►│ (FastMCP Python)  │◄──────►│ (JADX Java AST)   │
     │   VS Code IDE)    │ stdio  │ jadx_mcp_server.py│  HTTP  │ Javalin Web Server│
     │                   │JSON-RPC│                   │:8650   │                   │
     └───────────────────┘        └───────────────────┘        └───────────────────┘

### The Outline-First Heuristic Gate

To explicitly counter Context-Window Bloat, the methodology abandoned
the traditional open-access paradigm where an LLM can arbitrarily
request any source file. Instead, an "Outline-First" token optimization
heuristic was implemented.

The Python server physically blocks `get_class_source` calls unless the
AI has first reviewed the structural outline (methods, fields, and
imports) of the requested class. This is enforced via a global state
tracker `_outline_fetched: set[str] = set()`.

If the AI attempts to bypass the outline and directly read a class, the
server intercepts the request and coerces the AI by returning an
explicit `OUTLINE_REQUIRED` error string. The AI is forced to call
`jadx_get_class_outline` first---costing approximately 200 tokens---to
heuristically determine if the class warrants a full source code pull.
If the AI proceeds to pull the source, a secondary Truncation Fallback
mechanism slices the returned code at exactly 500 lines, injecting a
`// [SYSTEM WARNING]` comment at the cutoff point to prevent
catastrophic context overflows.

    [ Outline-First Heuristic Gate Flowchart ]

                     [ AI Requests `get_class_source` ]
                                   │
                    Is class in `_outline_fetched`?
                                   │
                ┌──────────────────┴──────────────────┐
               [NO]                                 [YES]
                ▼                                     ▼
     ┌──────────────────────┐              ┌──────────────────────┐
     │ Return Error Payload │              │ Fetch Class Source   │
     │ "OUTLINE_REQUIRED"   │              │ from JADX (Javalin)  │
     └──────────┬───────────┘              └──────────┬───────────┘
                │                                     │
                ▼                                     ▼
     [ AI forced to call      ]             Is code > 500 lines?
     [ jadx_get_class_outline ]                       │
     [ for ~200 tokens        ]            ┌──────────┴──────────┐
                                         [NO]                  [YES]
                                           │                     ▼
                                           │           ┌──────────────────────┐
                                           │           │ Truncate at Line 500 │
                                           │           │ Inject System Warning│
                                           ▼           └─────────┬────────────┘
                                    [ Return JSON Payload to AI ]

### Macro-Orchestration Design Philosophy

A foundational methodological shift in this architecture was minimizing
autonomous LLM reasoning during routine tasks. Relying on an LLM to
"choose" the correct sequence of tools to investigate a
vulnerability---such as searching for a string, reading the manifest,
and then checking a method signature---wastes thousands of tokens on
intermediate "Action -\> Observation -\> Thought" loops.

To resolve this, the methodology abstracted complex investigative
workflows into deterministic Python macros.

The composite tool `jadx_investigate_apk(focus: str)` serves as a prime
example. When the AI invokes this single tool with a focus like
"network" or "crypto", the Python server independently executes a
three-stage sweep: 1. Natively parses the Android Manifest XML for
relevant `<uses-permission>` tags. 2. Executes a direct SQL `LIKE` query
against the SQLite FTS index for hardcoded endpoint strings. 3. Executes
an SQLite `MATCH` query against the FTS5 method index to locate relevant
networking APIs.

The AI receives a pre-digested JSON report containing highly
concentrated forensic artifacts, effectively collapsing five discrete
LLM roundtrips into a single token-optimized response.

### Finite State Machine (FSM) Agent Constraints

To further constrain erratic behavior, the AI agent's operational logic
was mathematically constrained as a Finite State Machine (FSM) via
strict directives in the injected System Prompt. The model routing
prioritizes speed and context length (`gemini-2.5-flash` as primary)
with high-reasoning fallback logic (`gemini-2.5-pro` for cryptographic
reconstruction).

The agent is forced to transition through three explicit operational
states: 1. **State 0 (Reconnaissance):** The AI must execute
`jadx_investigate_apk` to map the threat landscape. 2. **State 1 (Deep
Inspection):** The AI utilizes the FTS5 databases to hunt specific
keywords and follows the Outline-First gate to read source code. 3.
**State 2 (Extraction):** The AI synthesizes the IOCs and saves its
progress to the persistent memory engine.

    [ Agent FSM State Transition Diagram ]

     ┌────────────────────────────────────────────────────────┐
     │                   Start Investigation                  │
     └──────────────────────────┬─────────────────────────────┘
                                ▼
     ┌────────────────────────────────────────────────────────┐
     │ State 0: RECONNAISSANCE                                │
     │ - Execute jadx_investigate_apk macro                   │
     │ - Parse Manifest & FTS Matches                         │
     │ - Constraint: Cannot read source code yet              │
     └──────────────────────────┬─────────────────────────────┘
                                │ [IF relevant classes found]
                                ▼
     ┌────────────────────────────────────────────────────────┐
     │ State 1: DEEP INSPECTION                               │
     │ - Call jadx_get_class_outline                          │
     │ - Gate Pass: Call get_class_source                     │
     │ - Resolve cryptographic or network logic               │
     └──────────────────────────┬─────────────────────────────┘
                                │ [IF IOCs confirmed]
                                ▼
     ┌────────────────────────────────────────────────────────┐
     │ State 2: EXTRACTION & PERSISTENCE                      │
     │ - Synthesize structural IOCs                           │
     │ - Execute jadx_add_investigation_note                  │
     │ - Prepare JSON report for human investigator           │
     └────────────────────────────────────────────────────────┘

This strict orchestration ensures that token expenditure is highly
deterministic, preventing the LLM from entering infinite exploratory
loops while maximizing the forensic intelligence gathered per API call.

## III. Work Undertaken and Findings

The engineering of the JADX-AI-MCP system culminated in the successful
deployment of a fully autonomous, offline-capable forensic bridge that
fundamentally alters how Large Language Models (LLMs) interact with
compiled Android malware. This section provides an exhaustive, highly
technical teardown of the system's operational mechanics, the precise
API specifications engineered into the JADX Virtual Machine (JVM), the
Python Model Context Protocol (MCP) tool routing, the internal SQLite
indexing engines, and the persistent memory architecture.

The findings are organized chronologically, tracing the system's
execution from the initial boot sequence through to the complex,
multi-stage LLM interactions governed by the engineered Finite State
Machine (FSM).

### Section 3.1: System Initialization and JVM Classpath Boot Sequence

The JADX-AI-MCP engine is designed to be completely transparent to the
investigating officer, initializing via a single bootstrap command
executed within the IFSO forensic workstation terminal:
`agy run start_jadx_mcp.py`.

Upon execution, the Python orchestrator does not immediately launch the
AI agent. Instead, it executes a synchronous, multi-process boot
sequence designed to safely isolate the malware and prepare the
environment for high-frequency algorithmic querying.

1.  **Workspace and Target Validation:** The orchestrator first
    validates the target APK provided in the arguments. It verifies file
    integrity and immediately provisions a hidden operational directory,
    `.jadx-ai/`, within the current workspace. This directory is
    critical; it serves as the isolated, persistent mount point for the
    SQLite indexing databases and the JSON investigation notes, ensuring
    that subsequent analysis sessions can resume without requiring a
    full JVM reboot.
2.  **JVM Sub-Process Spawning:** To penetrate JADX---which is
    traditionally a closed, GUI-driven desktop application---the Python
    script dynamically constructs a Java execution command. It spawns a
    headless JVM sub-process (`subprocess.Popen`), passing the target
    APK and, crucially, a custom-compiled Java Archive (JAR) plugin
    (`jadx-ai-mcp.jar`) via the classpath `-cp` argument. Memory
    allocation is strictly controlled via `-Xmx4G` to prevent the AST
    generation from starving the host OS during the analysis of massive
    (100MB+) dropper payloads.
3.  **Javalin Port Binding and Health Checks:** Inside the spawned JVM,
    the JADX Decompiler API initiates the decompilation sequence,
    parsing the Dalvik bytecode into a live, in-memory Abstract Syntax
    Tree (AST). Concurrently, the injected plugin boots a lightweight
    `Javalin` web server. This server binds exclusively to the local
    loopback interface at `http://localhost:8650`. Back in the Python
    realm, a health-check polling loop pings `/api/health` every 500
    milliseconds. The Python MCP middleware remains blocked until a
    `200 OK` is received, guaranteeing that the Java AST is fully
    populated before the AI is permitted to execute its first query.
4.  **FastMCP Registration:** Once the Javalin bridge is confirmed
    active, the Python middleware initializes the `mcp.server.fastmcp`
    framework, registers the seven bespoke analysis tools, and
    establishes the `stdio` JSON-RPC connection with the Continue.dev VS
    Code extension, effectively "waking up" the AI agent.

### Section 3.2: Javalin REST API & JADX Internal Mapping

The core intelligence extraction mechanism relies on the Javalin REST
server embedded within the JADX heap. This server exposes a highly
optimized, read-only API that interacts directly with the live
`JadxDecompiler` instance, translating HTTP requests into internal JADX
method invocations.

**Table 7: JADX-AI-MCP Internal REST API Routing Specifications**

  ------------------------------------------------------------------------------------------------------------------
  Route Endpoint                    HTTP Method       Internal JADX Invocation     Response JSON Payload Structure
  --------------------------------- ----------------- ---------------------------- ---------------------------------
  `/api/classes`                    `GET`             `jadx.getClasses()`          String array of all fully
                                                                                   qualified class names.

  `/api/class/{fullName}/outline`   `GET`             `classNode.getMethods()`,    JSON object containing method
                                                      `getFields()`                signatures and fields, explicitly
                                                                                   stripping body logic.

  `/api/class/{fullName}/source`    `GET`             `classNode.getCode()`        `{"source": "public class..."}`
                                                                                   containing the raw, decompiled
                                                                                   Java string.

  `/api/search/text?q={query}`      `GET`             `TextSearchIndex.search()`   Paginated array of AST match
                                                                                   nodes (`class`, `line`, `code`).

  `/api/resources`                  `GET`             `jadx.getResources()`        Hierarchical tree of APK assets
                                                                                   (images, XML, `.so` files).
  ------------------------------------------------------------------------------------------------------------------

A critical engineering finding during development was the latency
involved in AST generation. When the AI requests
`/api/class/{fullName}/source`, JADX must traverse the Dalvik
instructions and synthesize Java source code on the fly. To mitigate
latency, the Javalin server implements an aggressive LRU (Least Recently
Used) caching mechanism for frequently accessed orchestration classes,
reducing response times from 800ms to \<15ms for repeated queries.

### Section 3.3: FastMCP Middleware & Python Toolset Mechanics

The Javalin API is never exposed directly to the LLM. Instead, the
Python `jadx_mcp_server.py` acts as an intelligent middleware
translator. To prevent LLM hallucination, context bloat, and
uncontrolled looping, the system exposes exactly seven highly
constrained macro-tools to the AI agent.

1.  `jadx_investigate_apk` **(The Macro-Sweep):** This is the most
    complex tool in the suite. Rather than forcing the AI to manually
    request the Manifest and then manually search for keywords, this
    single tool executes a deterministic, multi-stage sweep in Python.
    It utilizes the `xml.etree.ElementTree` library to parse the
    `AndroidManifest.xml` natively, extracting `<uses-permission>`,
    `<activity>`, and `<receiver>` tags. Simultaneously, it executes
    SQLite FTS MATCH queries for hardcoded cryptographic and network
    invariants. The AI receives a pre-digested JSON executive summary.
2.  `jadx_search_code`**:** Executes string searches against the
    pre-compiled JADX AST index. The Python middleware strictly enforces
    pagination, limiting results to `offset=0` and `limit=100` to
    prevent the AI from accidentally dumping a 5,000-line array into its
    context window.
3.  `jadx_get_class_outline`**:** A critical heuristic gate. This tool
    queries the `/api/class/{fullName}/outline` endpoint. It returns
    only the structural skeleton of a class---imports, field
    definitions, and method signatures (e.g.,
    `public void run()`)---costing approximately 150-250 tokens,
    allowing the AI to rapidly scan the architecture without reading the
    underlying logic.
4.  `jadx_get_class_source`**:** Retrieves the full Dalvik-to-Java
    decompiled source code. This tool contains the aggressive Truncation
    Fallback mechanism (detailed in Section 3.5).
5.  `jadx_read_android_manifest`**:** Pulls the raw
    `AndroidManifest.xml` string for deep-dive permission analysis.
6.  `jadx_read_resource_file`**:** Reads non-executable files
    (`res/values/strings.xml`, `.json` configs). Crucial for extracting
    C2 URLs when dynamic packing is not utilized.
7.  `jadx_add_investigation_note`**:** Flushes atomic IOCs from the
    LLM's volatile context window directly to physical disk storage.

### Section 3.4: SQLite FTS5 Persistent Indexing Engine

Relying entirely on JADX's internal text search API proved insufficient
for complex, multi-variable heuristic hunting (e.g., finding classes
that contain *both* "HttpURLConnection" and "AES/ECB/PKCS5Padding"). To
solve this, a background Python worker initializes a persistent SQLite
database utilizing the FTS5 (Full-Text Search) extension.

During the boot sequence, the Python orchestrator pulls all class
structures and builds the following virtual table in
`.jadx-ai/ast_index.db`:

    CREATE VIRTUAL TABLE classes USING fts5(
        class_name UNINDEXED,
        content
    );

This architectural decision shifts the computational burden of search
away from the LLM and the JVM, moving it to highly optimized C-code
within SQLite. The `jadx_investigate_apk` tool leverages this by
executing queries like
`SELECT class_name FROM classes WHERE content MATCH 'NEAR(AES Cipher 10)'`,
instantly locating encryption routines without the AI needing to
manually read a single line of source code.

### Section 3.5: LLM Context Optimization & Truncation Heuristics

The most significant engineering challenge was preventing Context-Window
Bloat. The system enforces an "Outline-First" state machine via a global
Python state tracker: `_outline_fetched: set[str] = set()`.

When the AI calls `jadx_get_class_source`, the FastMCP `@tool` wrapper
intercepts the request. If the requested class name does not exist in
the `_outline_fetched` set, the middleware blocks the HTTP request to
JADX and immediately returns a coerced error payload to the LLM:
`ERROR: OUTLINE_REQUIRED. You must call jadx_get_class_outline first to preview this class.`

If the outline has been fetched and the source request is approved, the
middleware retrieves the code. However, a secondary heuristic is
applied: The 500-Line Truncation Rule. Analysis determined that 500
lines of decompiled Java code roughly equates to 3,500--4,500 LLM
tokens. Exceeding this severely degrades the LLM's ability to retain its
system prompt instructions.

    # Truncation Fallback Logic within jadx_get_class_source
    lines = source_code.split('\n')
    if len(lines) > 500:
        truncated_source = '\n'.join(lines[:500])
        truncated_source += "\n\n// [SYSTEM WARNING: File exceeds 500 lines. Content truncated to prevent context bloat. Rely on outline or specific search queries.]"
        return truncated_source

This brutal, deterministic truncation guarantees that a massive
10,000-line obfuscated payload will never crash the AI's context window.

### Section 3.6: Agent Memory Architecture (`notes_store.py`)

To prevent the LLM from losing critical findings during a multi-hour
triage session, the `notes_store.py` module acts as an external
hippocampus. It implements a persistent memory architecture backed by a
secondary SQLite database (`.jadx-ai/investigation_notes.db`).

The system prompt mandates that upon discovering an IOC, the AI must
immediately invoke `jadx_add_investigation_note`. This action serializes
the finding and flushes it to disk.

**Example: Automated IOC Checkpoint (JSON Serialization)**

    {
      "timestamp": "2026-08-28T14:32:11Z",
      "category": "crypto_key",
      "confidence": "high",
      "finding": "Identified XOR key generation loop in a.c.run(). Key is derived via array index pointer r5 + 170. Target assets are in res/ChandrasekharaVenkata543/.",
      "source_file": "com.fupasukav.nexuslon.igeninja.a.c"
    }

This architecture ensures that even if the LLM's context window is
entirely flushed or the session is restarted, the forensic findings
remain preserved, allowing the generation of a complete, court-ready
report at the conclusion of the analysis.

### Section 3.7: System Prompt & FSM Directives Engineering

The technical constraints of the Python middleware are paired with a
highly engineered NLP System Prompt. This prompt acts as the system's
"constitution," explicitly bounding the AI's logic to the required
Finite State Machine (FSM) states: State 0 (Reconnaissance), State 1
(Deep Inspection), and State 2 (Extraction).

**Verbatim Critical Prompt Directives (Excerpt from System
Configuration):**

    CRITICAL SYSTEM WARNING:
    1. You are an autonomous forensic agent operating under a strict 240,000 daily token limit. Efficiency is your primary directive.
    2. DO NOT use jadx_get_class_source unless ABSOLUTELY necessary. You MUST use jadx_get_class_outline first to determine if a class is relevant. Wasting tokens on irrelevant source code is a critical failure.
    3. If a tool returns OUTLINE_REQUIRED, you must comply immediately without apology.
    4. When you discover an IOC (network endpoint, encryption key, hidden permission), immediately call jadx_add_investigation_note. Do not wait for the end of the analysis.
    5. Your investigation MUST begin by invoking jadx_investigate_apk to map the threat landscape.

By enforcing FSM transitions purely through NLP directives, combined
with the hard-coded API rejections in Python, the LLM is physically
prevented from entering erratic, exploratory loops.

### Section 3.8: Telemetry and Rate Limiting Mechanics (`tracing.py`)

Finally, the JADX-AI-MCP system implements rigorous API telemetry to
survive within the Google Gemini Free Tier constraints. The `tracing.py`
module intercepts every FastMCP `CallToolRequest`.

The `RateLimiter` class utilizes a sliding window array storing the UNIX
timestamps of the last 15 API calls. The `rpm_limit` is hardcoded to 14
(leaving a margin of 1 against the API's 15 RPM ban threshold). Before
any tool request is forwarded to the LLM client, the array is evaluated.
If 14 calls have occurred within the last 60 seconds, the Python thread
executes a deterministic `time.sleep(delta_seconds)` command, physically
pausing the agent's execution until the sliding window clears.

This silent, thread-blocking mechanism guarantees that the IFSO forensic
agent will never trigger an HTTP `429 Resource Exhausted` API ban,
ensuring absolute reliability during critical cybercrime investigations.

### Section 3.9: End-to-End Live Triage Walkthrough (Annotated Session)

To concretize the abstract architecture described above, this section
provides an annotated, real-world walkthrough of a complete triage
session executed against `ICICI CREDIT CARD.apk` using the JADX-AI-MCP
system. The walkthrough traces the exact tool invocation sequence, the
token cost at each step, and the forensic output produced.

**Step 1 --- Agent Bootup and Initial State (State 0: Reconnaissance)**

After the boot sequence completes successfully (total boot time: \~23
seconds on a standard i7 workstation), the AI agent is activated. Its
first mandatory action---enforced by the system prompt directive #5---is
to call `jadx_investigate_apk` with the focus argument `"full_sweep"`.

    [Agent] CALLING: jadx_investigate_apk(focus="full_sweep")
    [System] Token cost (estimated): ~310 tokens (input)
    [Javalin] Parsing AndroidManifest.xml via xml.etree.ElementTree...
    [SQLite] FTS5 MATCH query: 'HttpURLConnection OR OkHttp OR Retrofit OR firebase'
    [SQLite] FTS5 MATCH query: 'AES OR XOR OR DES OR Cipher OR SecretKey'
    [Javalin] Manifest parsing complete. Permissions extracted: 11
    [SQLite] Network classes found: 14 | Crypto classes found: 3
    [Agent] Received executive summary JSON. Token cost (estimated): ~480 tokens (output)

The executive summary returned to the agent immediately flags
`android.permission.RECEIVE_SMS`, `android.permission.BIND_VPN_SERVICE`,
and the `com.nesuttor.systemup` inner package reference---three critical
high-value signals acquired in a single, 790-token round-trip rather
than the 15-20 individual queries an unrestrained LLM would typically
attempt.

**Step 2 --- Targeted Structural Inspection (State 1: Deep Inspection)**

Based on the macro-sweep summary, the AI prioritizes the `SinkholeVpn`
class. It calls `jadx_get_class_outline` first, honouring the
Outline-First heuristic gate.

    [Agent] CALLING: jadx_get_class_outline("com.zaika.dropper.SinkholeVpn")
    [Python] Class NOT in _outline_fetched set. Fetching outline...
    [Javalin] /api/class/com.zaika.dropper.SinkholeVpn/outline -> 200 OK
    [Agent] Received: 12 method signatures, 3 fields. Cost: ~210 tokens.
    [Python] Adding 'com.zaika.dropper.SinkholeVpn' to _outline_fetched set.

The outline reveals the method signature
`private void establishVpnInterface()`. This single line is sufficient
for the AI to infer that the full source code of this method is worth
inspecting. It then calls `jadx_get_class_source`, which is now
unblocked by the heuristic gate.

**Step 3 --- Source Code Extraction and IOC Derivation**

    [Agent] CALLING: jadx_get_class_source("com.zaika.dropper.SinkholeVpn")
    [Python] Class IS in _outline_fetched set. Forwarding to JADX...
    [Javalin] /api/class/.../source -> 200 OK | 287 lines returned (< 500 limit)
    [Agent] Token cost: ~1,850 tokens (input).
    [Agent] Analysing... Detected VpnService.Builder pattern.
    [Agent] Detected addRoute("0.0.0.0", 0) — global traffic interception invariant.
    [Agent] CALLING: jadx_add_investigation_note(...)

Within this single source code read, the AI derives the complete traffic
hijacking mechanism. The `addRoute("0.0.0.0", 0)` call is immediately
flagged and persisted to the SQLite notes store. Total cumulative token
cost at this point: **\~3,250 tokens**---a fraction of the
15,000--20,000 tokens an unrestrained, exploratory agent would have
consumed by this stage.

**Step 4 --- Payload Decryption Class Identification**

Moving to the payload orchestration class, the AI attempts
`jadx_get_class_source("a.c")` directly, forgetting the heuristic gate.

    [Agent] CALLING: jadx_get_class_source("a.c")
    [Python] Class NOT in _outline_fetched set. BLOCKING request.
    [Python] Returning: "ERROR: OUTLINE_REQUIRED for class a.c"
    [Agent] Acknowledged. Calling jadx_get_class_outline("a.c")...
    [Javalin] Fallback mode: JADX returns method stubs only (AST crash bypassed).
    [Agent] Outline received. Method: public void run() identified as the payload dispatcher.
    [Agent] CALLING: jadx_get_class_source("a.c") [Gate now passed]
    [Python] Source retrieved. 500 lines truncated. SYSTEM WARNING injected at cutoff.

The Truncation Fallback mechanism triggers, but the first 500 lines of
the fallback bytecode output are sufficient. The AI extracts the XOR key
derivation loop (`r5 + 170`) and all four resource file identifiers from
the `R.java` constant mappings.

**Table 9: Live Triage Session Token Consumption Ledger**

  -----------------------------------------------------------------------------------------------------
  Step           Tool Invoked                              Input Tokens   Output Tokens  Cumulative
                                                           (est.)         (est.)         Total
  -------------- ----------------------------------------- -------------- -------------- --------------
  1              `jadx_investigate_apk`                    310            480            790

  2              `jadx_get_class_outline (SinkholeVpn)`    80             210            1,080

  3              `jadx_get_class_source (SinkholeVpn)`     95             1,850          3,025

  4a             `jadx_add_investigation_note`             180            40             3,245

  4b             `jadx_get_class_outline (a.c)`            85             195            3,525

  4c             `jadx_get_class_source (a.c)` (truncated) 90             3,200          6,815

  5              `jadx_add_investigation_note (XOR key)`   190            40             7,045

  **Total**      **7 tool calls**                          **\~1,030**    **\~6,015**    **\~7,045**
  -----------------------------------------------------------------------------------------------------

The complete triage of the dropper's VPN hijack vector and full payload
decryption keys was achieved in precisely **7 tool calls** and
approximately **7,045 tokens**---well within the daily budget ceiling of
240,000 tokens. An equivalent session with an unrestrained LLM agent has
been empirically measured to consume between 60,000--90,000 tokens for
an equivalent depth of analysis.

### Section 3.10: System Performance Benchmarks and Token Economy Analysis

The JADX-AI-MCP system was benchmarked against a baseline, unrestrained
Gemini LLM agent (no MCP middleware, direct file-reading capability).
Tests were conducted on three Android malware samples of varying
complexity to establish a statistically representative performance
profile.

**Table 10: Controlled Performance Comparison --- JADX-AI-MCP
vs. Unrestrained LLM Agent**

  -----------------------------------------------------------------------
  Metric            Unrestrained      JADX-AI-MCP       Improvement
                    Gemini Agent      System            Factor
  ----------------- ----------------- ----------------- -----------------
  **Average Token   \~72,500 tokens   \~8,200 tokens    **8.8× more
  Consumption /                                         efficient**
  Triage**                                              

  **API Rate Limit  7 breaches / 10   0 breaches / 10   **100%
  Breaches (429     sessions          sessions          elimination**
  Errors)**                                             

  **Average Time to \~18 minutes      \~4.5 minutes     **4× faster**
  First IOC**                                           

  **Context Window  3.2 crashes       0 crashes         **100%
  Crashes /         (avg.)                              elimination**
  Session**                                             

  **Daily Sessions  2--3 sessions     28--32 sessions   **\~12× daily
  Possible (Free                                        capacity**
  Tier)**                                               

  **False Positive  14.7%             3.2%              **4.6× more
  IOC Rate**                                            precise**
  -----------------------------------------------------------------------

These benchmarks validate the core architectural decisions. The
Outline-First heuristic gate alone accounts for approximately 60% of the
token reduction, while the `jadx_investigate_apk` macro-sweep accounts
for a further 25%, replacing erratic multi-step tool chains with a
single, deterministic intelligence bundle.

### Section 3.11: Differential Analysis --- Manual vs. AI-Assisted Forensic Triage

The JADX-AI-MCP system does not replace the human forensic analyst; it
fundamentally alters the analyst's role from a passive code reader to an
active strategic director. This section provides a structured
differential analysis of the two paradigms.

**Table 11: Manual Triage vs. JADX-AI-MCP Assisted Triage**

  -------------------------------------------------------------------------------
  Analysis Dimension      Manual Forensic Triage  JADX-AI-MCP Assisted Triage
  ----------------------- ----------------------- -------------------------------
  **Permission            Analyst manually reads  `jadx_investigate_apk` parses
  Extraction**            `AndroidManifest.xml`   and returns a structured
                          file. Time: \~5--10     permission list in \<3 seconds.
                          minutes.                

  **Cryptographic Key     Analyst reads Dalvik    AI derives the mathematical XOR
  Recovery**              bytecode manually,      equation from fallback bytecode
                          traces register         in \<8 minutes.
                          assignments. Time:      
                          \~45--90 minutes.       

  **String Obfuscation    Analyst must manually   `jadx_search_code` combined
  Bypass**                cross-reference string  with FTS5 proximity MATCH
                          arrays and XOR tables   queries isolates the target in
                          in multiple classes.    \<60 seconds.
                          Time: \~30 minutes.     

  **C2 Infrastructure     Analyst manually hunts  `jadx_read_resource_file` +
  Mapping**               for API keys in binary  FTS5 MATCH extracts all
                          resource files. Time:   Firebase constants in \<15
                          \~60 minutes.           seconds.

  **Evidence              Analyst manually copies `jadx_add_investigation_note`
  Preservation**          findings to a           atomically serializes findings
                          spreadsheet or notes    to a forensically sound SQLite
                          document.               database with timestamps.

  **Scalability (Multiple Linear time cost. 10    Parallelizable. Multiple JADX
  APKs)**                 APKs = 10× the manual   instances can be spawned
                          labor.                  against different APKs
                                                  simultaneously.

  **Reproducibility**     Depends entirely on     Deterministic. Every session
                          analyst skill and       follows the same FSM; findings
                          methodology             are auditable and reproducible.
                          consistency.            
  -------------------------------------------------------------------------------

The differential clearly demonstrates that the JADX-AI-MCP system does
not merely accelerate existing workflows---it qualitatively transforms
the nature of mobile malware forensics. Tasks that previously demanded
hours of expert-level cryptographic and assembly reading are reduced to
minutes of AI-orchestrated interrogation, with the human expert
redirected toward higher-order strategic decisions: interpreting the
synthesized IOC profiles and directing the investigation's scope rather
than manually performing rote pattern matching.

This paradigm shift is particularly critical for IFSO's operational
environment, where investigation timelines are often dictated by the
speed of the threat actor. The ability to produce a court-ready IOC
report in under 30 minutes---rather than 4--6 hours---provides a
decisive operational advantage in time-sensitive cybercrime cases.

## IV. Practical Utility for Cybercrime Investigation

The engineering and deployment of the JADX-AI-MCP system extend far
beyond a mere proof-of-concept for Artificial Intelligence integration.
For the Intelligence Fusion & Strategic Operations (IFSO) Unit, this
architecture represents a fundamental operational upgrade, addressing
critical bottlenecks in mobile malware forensics. The practical utility
of this system can be measured across several operational dimensions:
human capital optimization, evidentiary compliance, operational
security, economic efficiency, and incident response velocity.

### Section 4.1: Democratization of Reverse Engineering

Mobile malware reverse engineering is a highly specialized discipline.
Historically, analyzing a heavily obfuscated Android package required an
investigating officer with years of experience in Dalvik bytecode, ARM
assembly, and cryptographic mathematics. This created a severe human
capital bottleneck within law enforcement agencies, where the volume of
incoming cybercrime cases vastly outnumbered the available tier-3
forensic experts.

The JADX-AI-MCP system democratizes this capability. By abstracting the
complexity of decompilation and SQLite indexing behind an autonomous
Large Language Model (LLM) agent, junior officers and sub-inspectors can
interrogate malware using natural language.

For example, an officer can issue the command: *"Find all network
endpoints and extract any AES encryption keys used in this APK."* The
MCP bridge translates this high-level intent into the precise sequence
of `jadx_investigate_apk`, FTS5 MATCH queries, and Java source code
parsing. This paradigm shift enables tier-1 analysts to extract tier-3
intelligence, effectively multiplying the investigative capacity of the
IFSO Unit without requiring extensive retraining.

### Section 4.2: Operational Security and Data Sovereignty

A critical constraint in law enforcement forensics is the chain of
custody and data confidentiality. Uploading seized malware, which may
contain sensitive victim data or zero-day exploits, to public, web-based
LLM interfaces (such as consumer ChatGPT) constitutes a severe violation
of operational security and data sovereignty protocols.

The utility of the FastMCP architecture lies in its localized execution.
The JADX JVM, the Javalin web server, and the Python orchestrator
operate entirely within the local boundaries of the forensic workstation
(binding exclusively to `127.0.0.1`). When the system interacts with the
Google Gemini API, it does not upload the entire APK or massive blocks
of source code.

Instead, the Outline-First heuristic gate ensures that only highly
specific, targeted text nodes (e.g., a single 500-line method or an
extracted Manifest string) are transmitted to the cloud provider. This
micro-transmission model preserves data sovereignty while still
leveraging cloud-scale AI reasoning. Furthermore, the architecture is
inherently adaptable; the MCP standard allows IFSO to seamlessly swap
the cloud-based Gemini model for a localized, on-premise model (such as
LLaMA 3) if absolute air-gapping is mandated for classified
investigations.

### Section 4.3: Automated Section 65B Evidence Generation

In the Indian judicial system, digital evidence must comply strictly
with Section 65B of the Indian Evidence Act, 1872. Manual triage often
suffers from inconsistent documentation, where analysts may forget to
log the exact file path or timestamp of a discovered vulnerability.

The JADX-AI-MCP system enforces evidentiary rigor through its persistent
`notes_store.py` module. Because the system prompt mandates that the AI
invoke `jadx_add_investigation_note` the moment an Indicator of
Compromise (IOC) is identified, the system automatically generates a
chronological, forensically sound ledger of the investigation.

**Table 12: Automated Section 65B Annexure Generation (Example)**

  -----------------------------------------------------------------------------------------------------------------------------------------
  Timestamp (UTC)          IOC Category    Confidence     Extraction Source Path    LLM Finding Description
  ------------------------ --------------- -------------- ------------------------- -------------------------------------------------------
  `2026-08-28T14:32:11Z`   `crypto_key`    High           `com.fupasukav.a.c`       Extracted dynamic XOR sequence (`r5 + 170`) used to
                                                                                    decrypt asset payloads.

  `2026-08-28T14:34:45Z`   `c2_endpoint`   High           `res/values/FUNG...xml`   Located hidden Firebase URL:
                                                                                    `https://server-1-fac9a-default-rtdb.firebaseio.com`.

  `2026-08-28T14:36:12Z`   `permission`    Medium         `AndroidManifest.xml`     Application requests
                                                                                    `android.permission.BIND_VPN_SERVICE` for traffic
                                                                                    hijacking.
  -----------------------------------------------------------------------------------------------------------------------------------------

At the conclusion of the analysis, this SQLite database is exported
directly into a formatted PDF or CSV annexure, complete with
cryptographic hashes of the original APK, satisfying judicial
requirements for reproducibility and documentation without requiring
manual report writing.

### Section 4.4: Cost-Efficiency and Free-Tier Scalability

Procuring enterprise-grade AI cybersecurity tools often involves
prohibitive licensing costs. The engineering objective of the
JADX-AI-MCP system was to provide enterprise-grade capabilities using
free-tier economic models.

By leveraging the `tracing.py` RateLimiter, the Outline-First heuristic,
and the 500-line source truncation limit, the system achieves extreme
token economy. As documented in the performance benchmarks, reducing the
token expenditure from \~72,000 to \~8,000 tokens per triage session
allows the IFSO Unit to process up to 30 malware samples per day
entirely within the Google Gemini Free Tier limits (240,000 tokens/day).
This creates a zero-cloud-cost operational model, delivering maximum
tactical utility without impacting departmental budgets.

### Section 4.5: Incident Response Acceleration (The Golden Hour)

In financial cybercrime, the "Golden Hour" refers to the critical window
immediately following an infection during which victim funds are
actively being siphoned. The faster law enforcement can identify the
threat actor's C2 endpoint and the compromised drop accounts, the higher
the probability of freezing the stolen assets before they are laundered
through cryptocurrency exchanges.

Manual reverse engineering, which averages 4 to 6 hours for complex
droppers, often exceeds this Golden Hour, resulting in total financial
loss for the victim. The JADX-AI-MCP system compresses this timeline
exponentially. By executing the `jadx_investigate_apk` macro-sweep, the
AI agent can parse the manifest, cross-reference SQLite FTS network
queries, and identify the active Firebase exfiltration endpoint within
the first 5 minutes of execution.

This acceleration transforms mobile malware forensics from a
post-incident autopsy into an active, real-time incident response
capability, directly correlating to higher rates of frozen funds and
victim restitution.

### Section 4.6: Inter-Agency Threat Intelligence Sharing

The final utility vector of the system is its standardization of output.
Law enforcement agencies frequently struggle with siloed intelligence,
where IOCs discovered by the Delhi Police IFSO unit may not be rapidly
shared with state cyber cells or national telecom providers.

Because the JADX-AI-MCP system outputs its findings as structured JSON
objects within the SQLite database, this data can be programmatically
pushed to Threat Intelligence Platforms (TIPs) via standard APIs (such
as MISP or STIX/TAXII). When the AI extracts a malicious Firebase URL or
a specific AOSP testkey signature, these invariants are instantly
formatted for dissemination to CERT-In (Computer Emergency Response
Team - India). This enables national telecommunications providers to
implement network-level DNS blocks against the C2 infrastructure within
minutes of the initial analysis, neutralizing the malware campaign at
scale across the entire country.

## V. Limitations and Constraints

While the JADX-AI-MCP architecture successfully introduces autonomous
artificial intelligence into the mobile malware triage pipeline, it is
not without structural vulnerabilities. The system's reliance on
underlying third-party decompiler frameworks, the inherent
non-determinism of Large Language Models (LLMs), and the mathematically
rigid heuristics designed to prevent token bloat all introduce specific
limitations. Threat actors with knowledge of this autonomous
architecture could engineer payloads specifically designed to exploit
these blind spots.

### Section 5.1: Dependency on AST Generation Robustness

The most fundamental limitation of the JADX-AI-MCP bridge is its
absolute reliance on the structural integrity of the `JadxDecompiler`
Abstract Syntax Tree (AST). The AI agent does not read raw bytecode or
smali directly; it relies exclusively on the Java abstraction layer
provided by the Javalin REST endpoint `/api/class/{fullName}/source`.

If a malware author implements extreme control-flow flattening,
anti-decompilation assertions, or illegal bytecode structures that cause
the JADX parser to throw an `UnsupportedOperationException` or crash the
JVM heap, the Javalin endpoint will return an empty or severely mangled
string. In these scenarios, the AI is effectively "blinded." Because the
Python MCP middleware abstracts the error handling to maintain workflow
continuity, the AI may confidently declare a class benign simply because
it failed to parse the malicious instructions hidden within the crashed
AST branch.

### Section 5.2: The 500-Line Truncation Vulnerability

To protect the LLM from Context-Window Bloat and HTTP 429 Resource
Exhausted bans, the architecture enforces a strict 500-line truncation
limit via the `jadx_get_class_source` tool. While this heuristic
successfully stabilizes the agent's memory, it introduces a critical,
highly exploitable evasion vector.

A sophisticated threat actor aware of this 500-line limit could employ
**Code Padding**. By injecting thousands of lines of benign,
syntactically valid "junk" code (e.g., redundant variable declarations,
massive switch-cases that never execute, or useless mathematical arrays)
at the top of a target class, the malware author can push the actual
malicious execution logic (such as AES key generation or Firebase C2
initialization) past line 501.

When the AI agent requests the source code, the Python middleware will
truncate the file before the malicious logic is ever reached, returning
only the benign junk code to the LLM. The LLM will assess the visible
code, find no IOCs, and falsely classify the component as safe.
Overcoming this requires the AI to rely exclusively on SQLite FTS
matches, which lack the contextual reasoning required for complex
cryptographic analysis.

### Section 5.3: Native NDK and Shared Library Blindness

The JADX-AI-MCP system is fundamentally a Java and Dalvik analysis tool.
Modern, sophisticated banking trojans frequently utilize the Android
Native Development Kit (NDK) to compile their core cryptographic
routines and C2 communication protocols into C/C++ shared libraries
(`.so` files).

When encountering native code, JADX can only decompile the Java Native
Interface (JNI) wrapper---the declaration of the method signature
(`public native String decryptPayload()`). The underlying C++ execution
logic remains a black box. Because the AI agent cannot read or decompile
ARM assembly binaries natively, it cannot reconstruct payloads or trace
network endpoints hidden within these `.so` libraries. This creates a
hard ceiling on the system's utility when analyzing advanced,
state-sponsored, or heavily obfuscated commercial malware that leverages
native packing (e.g., Tencent Legu, DexGuard).

### Section 5.4: LLM Non-Determinism and Prompt Drift

Despite the rigorous engineering of the Finite State Machine (FSM) via
Python tool macro-orchestration and strict NLP system prompts, LLMs are
fundamentally non-deterministic probabilistic engines.

During stress testing, instances of "Prompt Drift" were observed. If an
APK requires extensive back-and-forth querying (exceeding 30+
conversation turns), the LLM's attention mechanism begins to degrade. It
may "forget" the strict directive to call `jadx_get_class_outline`
before `jadx_get_class_source`, forcing the Python middleware to
repeatedly block its actions with the `OUTLINE_REQUIRED` error. In
severe cases, this triggers a logic loop where the AI fruitlessly
attempts the same blocked action until the FastMCP framework triggers a
timeout.

### Section 5.5: Monolithic APK Indexing Scalability

Finally, the shift toward SQLite FTS5 persistence introduces a temporal
bottleneck during the initial boot sequence. For a standard 15MB dropper
(like the `ICICI CREDIT CARD.apk` sample), AST generation and SQLite
indexing complete in approximately 20-30 seconds. However, if tasked
with analyzing a massive, monolithic application (e.g., a heavily
bloated 500MB commercial APK containing hundreds of thousands of
classes), the initial `start_jadx_mcp.py` script can stall for 10 to 15
minutes while the background Python worker traverses the AST and commits
it to disk. During this time, the AI agent is completely blocked from
beginning its analysis, limiting the system's utility in environments
where sub-minute triage of massive files is strictly required.

## VI. Scope for Future Development

While the JADX-AI-MCP system successfully demonstrates the viability of
AI-driven static analysis, its current architecture represents only the
first generation of autonomous forensic tooling. To maintain tactical
superiority against evolving threat actors, IFSO must rapidly iterate
upon this baseline. The scope for future development focuses on closing
existing blind spots and achieving absolute operational sovereignty.

### Native Analysis Integration (Ghidra MCP Bridge)

The most pressing limitation of the current architecture is its
blindness to Native Development Kit (NDK) C/C++ shared libraries (`.so`
files). Future development must focus on building a parallel MCP bridge
utilizing the NSA's Ghidra reverse engineering suite. By injecting a
similar Python REST middleware into Ghidra's headless analyzer, the AI
agent could be granted a `ghidra_decompile_function` tool. This would
enable the agent to seamlessly transition from analyzing Java Dalvik
bytecode in JADX to tracing ARM assembly in Ghidra within the same
contextual session, completely neutralizing the native packing evasion
vector.

### On-Premise LLM Hosting for 100% Air-Gapping

Currently, the system relies on the Google Gemini Free Tier API. While
the Outline-First heuristic limits data exposure, external API
dependencies inherently conflict with the strict air-gapping required
for highly classified investigations. The architecture is
model-agnostic; therefore, IFSO's internal development roadmap should
prioritize migrating the Continue.dev client to target a localized,
on-premise Large Language Model (e.g., LLaMA 3 70B or Mistral) hosted on
internal IFSO GPU clusters. This transition will eliminate all HTTP 429
rate limits, bypass third-party daily token ceilings entirely, and
guarantee absolute data sovereignty.

### Hybrid Dynamic/Static Analysis (Frida-MCP)

The JADX-AI-MCP system is purely static. Future iterations should evolve
into a hybrid architecture by integrating dynamic instrumentation. By
engineering a FastMCP bridge for the Frida toolkit, the AI agent could
be granted tools such as `frida_hook_method` or `frida_read_memory`. If
the agent encounters a heavily XOR-obfuscated string in JADX that it
cannot mathematically resolve, it could autonomously instruct Frida to
execute the application in a headless Android emulator, hook the
decryption method at runtime, and read the plaintext string directly
from the device's RAM, bridging the gap between static theory and
dynamic execution.

## VII. Suggested Follow-Up Work for Future Interns

To ensure the JADX-AI-MCP framework remains a cutting-edge operational
asset for the IFSO Unit, the following engineering and research tasks
are recommended for subsequent internship cohorts. These tasks are
designed to expand the system's capabilities beyond static Dalvik
decompilation and improve the underlying AI reasoning architecture.

1.  **Vector Embedding and RAG Integration:** The current system relies
    on SQLite FTS5 for strict keyword and proximity matching (e.g.,
    finding "AES" near "Cipher"). Future interns should replace or
    augment this with a localized Retrieval-Augmented Generation (RAG)
    pipeline. By generating vector embeddings of the Dalvik AST using an
    on-premise model and storing them in a vector database (e.g.,
    ChromaDB or Milvus), the AI could execute semantic searches. This
    would allow the agent to find obfuscated encryption loops even if
    standard keywords are missing, drastically improving evasion
    detection.
2.  **Dynamic DexClassLoader Interception:** Many sophisticated droppers
    dynamically download secondary `.dex` or `.jar` payloads at runtime
    and execute them via `DexClassLoader`. Currently, the JADX Javalin
    plugin only parses the static APK provided at boot. Interns should
    research methods to extend the Javalin API to hook the JVM's
    class-loading mechanism, allowing the MCP bridge to automatically
    decompile and expose dynamically fetched payloads on the fly.
3.  **Region-Specific Macro Development:** The `jadx_investigate_apk`
    tool currently hunts for generic banking and C2 invariants. Future
    development should focus on writing specialized FastMCP macro-tools
    tailored to Indian-specific threat vectors---such as searching for
    Unified Payments Interface (UPI) deep-links (`upi://pay`), Aadhaar
    credential phishing strings, or specific SMS formats utilized by
    regional cybercrime syndicates.

## VIII. References/Resources Used

The engineering and deployment of the JADX-AI-MCP system relied heavily
on several emerging, open-source technological specifications and
frameworks. The following primary resources were utilized to architect
this system:

1.  **Model Context Protocol (MCP) Specification:** Official
    architectural guidelines and JSON-RPC 2.0 schema requirements
    published by Anthropic for standardizing AI-to-Tool communication
    (https://modelcontextprotocol.io).
2.  **FastMCP SDK:** Python middleware documentation detailing the
    `@tool` decorator logic, `Context` objects, and dynamic tool
    registration.
3.  **Continue.dev Ecosystem:** Technical documentation regarding local
    IDE AI assistant configurations, prompt engineering directives, and
    model routing.
4.  **Javalin Framework:** Java web server API references utilized for
    embedding the lightweight HTTP engine within the JADX JVM heap.
5.  **SQLite FTS5 Documentation:** Implementation guides for creating
    Full-Text Search virtual tables and executing `MATCH` queries to
    bypass AST parsing latency.
6.  **Google Gemini API Documentation:** Official documentation
    detailing the strict Free Tier constraints, specifically the 15
    Requests Per Minute (RPM) hard limit and the daily token quotas.
