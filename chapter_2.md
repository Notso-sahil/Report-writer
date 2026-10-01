## 2.1 Problem Statement

The rapidly evolving threat landscape of mobile malware has seen a significant shift toward sophisticated, multi-stage dropper mechanisms that leverage brand impersonation to achieve high infection rates. A prime example is the pervasive banking impersonation dropper superficially packaged as `ICICI CREDIT CARD.apk`. These outer packages serve as benign-looking delivery vehicles designed solely to bypass initial automated security scans and establish deep device persistence. 

Once executed, these malicious droppers employ aggressive persistence mechanics, such as utilizing Android `InstallReceiver` components and programmatic UI rendering to trick users into granting invasive VPN permissions. This facilitates in-memory traffic hijacking (e.g., global route injection `0.0.0.0/0`), allowing the threat actor to intercept all inbound and outbound device communications.

The primary forensic challenge addressed in this project is the severe obstruction of static analysis. Modern malware authors deploy advanced obfuscation techniques—specifically **control-flow flattening** and **XOR payload encryption**—to intentionally crash standard decompilation tools like JADX. When JADX encounters these extreme flattening loops, its Abstract Syntax Tree (AST) thresholds are exhausted, resulting in catastrophic heuristic failures (`UnsupportedOperationException`). 

Simultaneously, manual forensic triage is heavily bottlenecked by the sheer volume of code. While large language models (LLMs) offer the potential for automated analysis, applying them to malware reverse engineering is severely restricted by context-window limitations, strict API token economics (especially on Free Tier limits), and the inability of LLMs to traverse massive Android project architectures natively. The core problem is therefore twofold: defeating advanced anti-analysis mechanisms in banking malware, and engineering an autonomous, AI-augmented triage system that scales effectively within strict computational constraints.

## 2.2 Software Design

To address these dual challenges, the project was conceptually divided into two distinct architectural domains: Threat Model Deconstruction and AI System Architecture.

**Domain A: Threat Model Deconstruction Architecture**
The forensic triage of the `ICICI CREDIT CARD.apk` dropper required a state-machine bypass design to transition from automated heuristics to manual cryptographic recovery:
- **Phase 1 (AST Bypass):** Forcing the JADX decompiler engine into "Fallback Mode" to expose raw Dalvik bytecode, bypassing the AST generation failures caused by control-flow flattening.
- **Phase 2 (Cryptographic Recovery):** Tracing register mutations (`r4`, `r5`, `r7`) to mathematically derive the bitwise XOR key ($Key = r5 + 170$) used to encrypt the secondary payload.
- **Phase 3 (Payload Unpacking):** Developing an offline decryption script to linearly stitch the fragmented, masked resource blocks (`.bin`, `.so`, `.dex`) back into the true malicious application package (`com.nesuttor.systemup`).

**Domain B: JADX-AI-MCP System Architecture**
To automate this forensic analysis across large codebases, the project designed the JADX-AI-MCP system, utilizing a Model Context Protocol (MCP) framework.
- **Dual-Language Topology:** The architecture bridges a Python-based intelligent agent (FastMCP) with a Java-based routing backend (Javalin).
- **Token Optimization:** Instead of feeding entire Android repositories to the LLM, the system uses an "Outline-First" heuristic, mapping class structures via a vectorless SQLite FTS5 index.
- **Strict Observability:** The design integrates a sliding-window rate limiter to cap execution (e.g., 14 RPM) and prevent API exhaustion, alongside OpenTelemetry span graphs for precise logging of the AI's decision trees.

## 2.3 Implementation

The implementation of this project translates the theoretical designs into actionable, code-driven execution pipelines used by the IFSO Unit.

For the malware decryption, the implementation involved writing precise Python automation that targets the obfuscated asset folder (`res/ChandrasekharaVenkata543/`), iterates over the four sequential fragments, applies the dynamic XOR matrix, and compiles the clean `decrypted_payload.apk`. Post-decryption, the implementation shifted to tracing the malware's backend telemetries, mapping the obfuscated Google Firebase C2 schema (`DJ_BABU/RBL_Admin_3`), and developing Fast-Triage Python scripts for investigating officers to intercept stolen SMS OTPs in real-time.

For the AI-automation system, the implementation focused on the cross-session state persistence engine (`notes_store.py`) which allows the LLM to save contextual clues across multiple JADX searches without forgetting previous findings. The Javalin backend was implemented to deterministically route the LLM's requests to the underlying JADX compilation engine, bypassing the need for manual UI interactions. 

By unifying deep Dalvik reverse engineering with structured, rate-limited AI automation, the project successfully delivered a robust methodology for deconstructing high-threat mobile malware while scaling investigative capacity.
