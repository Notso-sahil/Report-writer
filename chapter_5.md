## 5.1 Discussion & Practical Utility

The technical deconstruction of the `ICICI CREDIT CARD.apk` dropper and the subsequent development of the `JADX-AI-MCP` system are not merely academic exercises; their primary value lies in the immediate, actionable intelligence they provide to law enforcement agencies like the IFSO Unit. By transitioning from the raw bytecode analysis into a structured investigative workflow, cybercrime officers can actively monitor a threat actor's command-and-control (C2) infrastructure. 

The Fast-Triage workflow allows investigators to intercept compromised phone numbers and OTPs in real-time. By querying the exposed Firebase REST API, officers can parse out the specific victims being targeted by the `DJ_BABU` campaign and instantly notify nodal banking officers to freeze accounts before fraudulent transactions are completed. The AI-automation engine acts as a force multiplier, scaling this capability so that a single investigator can triage multiple massive malware campaigns simultaneously without manual burnout.

## 5.2 Future Scope

While the current dual-language MCP architecture effectively handles standard banking trojans, future iterations of this software must address more sophisticated packers like Tencent Legu or DexGuard. The scope for future development includes:
1. **Dynamic Unpacking Integration:** Bridging the MCP system with dynamic instrumentation frameworks like Frida to automatically dump decrypted Dex files from memory, bypassing the need for manual XOR key derivations.
2. **Local LLM Execution:** Transitioning away from cloud-based LLM APIs (to mitigate strict token limits and data privacy concerns) and integrating heavily quantized local models (such as Llama-3-8B-Instruct) directly onto the investigator's forensic workstation.
3. **Automated Takedown Pipelines:** Engineering outgoing API hooks that can autonomously generate and send legal takedown notices to infrastructure providers (like Google Cloud Platform) once malicious C2 endpoints are verified.

# References

1. Android Open Source Project (AOSP) Documentation. *VpnService Architecture and Implementation.*
2. Google Firebase SDK Developer Guide. *Realtime Database REST API Telemetry.*
3. JADX Decompiler Documentation. *AST Generation and Control-Flow Flattening Heuristics.*
4. MITRE ATT&CK Framework. *Mobile Matrix: T1407, T1418, T1437.*
5. Tiktoken. *OpenAI Tokenizer Economics and sliding window methodologies.*
