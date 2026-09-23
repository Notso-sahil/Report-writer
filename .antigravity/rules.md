# Antigravity System Directives & Forensic Agent Guardrails (.antigravity/rules.md)

## 1. Project Context & Author Identification
* **Author / Intern Name:** Sahil Yadav
* **Operational Unit:** Intelligence Fusion & Strategic Operations (IFSO) Unit, Special Cell, Delhi Police
* **Domain:** Cybercrime Investigation, Mobile Malware Reverse Engineering & Forensic Automation
* **Project Deliverable:** 40-Page Comprehensive Dossier containing Case Study 1 (Malicious Dropper Triage) and Case Study 2 (JADX-AI-MCP Architecture & Observability SOP)

---

## 2. Zero-Hallucination & Factual Grounding Policy
* **Source Fidelity:** Strictly ground all technical findings, class names, method signatures, package paths, and indicators of compromise (IOCs) on the provided source materials (`ICICI_Sahil.docx` and `Production_SOP_and_Architecture.docx`).
* **No Invented Artifacts:** Do NOT invent, guess, or extrapolate fictitious C2 endpoints, API keys, decryption constants, or file names. 
  * Case Study 1 constants must strictly match recovered values (e.g., XOR formula `Key = r5 + 170`, key sequence `0xAA` to `0xAD`, Firebase URL `https://server-1-fac9a-default-rtdb.firebaseio.com`, package `com.zaika.dropper` / `com.nesuttor.systemup`).
  * Case Study 2 constants must strictly match architecture values (e.g., Rate limits 14 RPM, 240,000 daily tokens, SQLite FTS5 schemas, port 8650, tiktoken `cl100k_base`).
* **Ambiguity Handling:** If an operational parameter or implementation nuance is absent, output `[MISSING CONTEXT: <Specify Requirement>]` and pause for clarification rather than hallucinating placeholder values.
* **No Code Skeletals:** Never output incomplete code blocks, truncated snippets, or comments such as `# TODO`, `// implement here`, or `...`. Every script, Lua block, SQL DDL, and Python class must be complete and syntactically valid.

---

## 3. Iterative Section Generation Protocol
* **Strict Single-Section Execution:** Never generate the entire 40-page report in a single output turn. Generate exactly one section/heading file at a time (e.g., `cs1_01_objective.md`, then `cs1_02_methodology.md`).
* **Review Gate:** Require explicit user verification and approval before moving to the next sequential section file.
* **Quantitative Budget Compliance:** Every section must fulfill its assigned page and word count budget before proceeding to ensure the compiled document naturally reaches 40 pages (~11,700–12,500 words).

---

## 4. Standardized 8-Heading Structural Mandate
For both Case Study 1 and Case Study 2, content must strictly map into the official 8-heading format:
* **I. Objective and Problem Statement** (Threat landscape, problem formulation, invariants)
* **II. Methodology Adopted** (Decompilation tooling, AST parsing, pipeline architecture)
* **III. Work Undertaken and Findings** (Deep technical breakdown, math proofs, DDL/code, tables)
* **IV. Practical Utility for Cybercrime Investigation** (Actionable SOP, evidentiary chain of custody)
* **V. Limitations/Challenges** (Anti-analysis evasion, AST crashes, compute constraints)
* **VI. Scope for Future Development** (Architectural scaling, automated unpackers)
* **VII. Suggested Follow-Up Work for Future Interns** (Actionable research and engineering tasks)
* **VIII. References/Resources Used** (RFCs, AOSP documentation, MITRE ATT&CK Mobile matrices)

---

## 5. Technical Artifact & 6-Layer Engineering Standard
Every core analytical module must be documented across the 6 technical layers:
1. **Mathematical Model & Algorithmic Basis** (XOR transformations, sliding-window equations, jitter formulas)
2. **Data Structures & Schemas** (Complete PostgreSQL/SQLite DDL, JSON Schemas, Redis namespaces)
3. **Execution Lifecycle & Flow** (Step-by-step ASCII pipelines and sequence transitions)
4. **Configuration Matrices** (Tabular parameters with data types, defaults, and trigger thresholds)
5. **Fault Tolerance & Edge Modes** (Handling AST failures, fallback bytecode, HTTP 429 backoff)
6. **Operational Runbooks & SOPs** (Runnable Bash, Redis CLI, and SQL diagnostic commands)

---

## 6. Document Formatting & Word Compilation Rules
* **Heading Hierarchy:** Use clean Markdown heading tags (`#` for document title, `##` for major sections, `###` for sub-sections) to allow clean compilation into Word (`.docx`).
* **Visual Scaffolding:** Include ASCII flow diagrams, structural directory trees, and markdown tables.
* **Page Break Injection:** Major sections must be separated by Word OpenXML page breaks:
  ```markdown
  ```{=openxml}
  <w:p><w:r><w:br w:type="page"/></w:r></w:p>
  ```
  ```