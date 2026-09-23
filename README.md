# Autonomous Large Technical Document & Report Generation Pipeline (Antigravity Framework)

A standardized, multi-phase framework for orchestrating AI Agents (such as Google Antigravity) to produce dense, production-grade technical reports, Standard Operating Procedures (SOPs), and multi-case study dossiers spanning **10 to 100+ pages** without artificial fluff, context truncation, or hallucinations.

---

## Quick-Start Invocations for New Users

When opening a new Antigravity session with this `README.md` attached, choose and paste one of the two standard entry prompts:

### Option A: Generating from a Codebase
```text
Read the guidelines in README.md. I have provided a codebase in `raw_sources/codebase/` and an image/spec of the required document structure. 

I need a production-grade Technical Architecture & SOP Report of exactly [X] pages.

Execute Step 1 and Step 2:
1. Analyze the codebase and generate `.antigravity/rules.md` with zero-hallucination guardrails.
2. Generate `project_blueprint.md` with a complete page/word allocation matrix and compilation script for [X] pages.
3. Present the Phased Implementation Plan for my approval before drafting any sections.
```

### Option B: Generating from Existing Documentation (`.docx` / Notes)
```text
Read the guidelines in README.md. I have uploaded source files in `raw_sources/` and an image/spec of the required report format. 

I need a unified, comprehensive Dossier/Report of exactly [X] pages expanding on these materials.

Execute Step 1 and Step 2:
1. Extract and map the source documents to the required format and generate `.antigravity/rules.md`.
2. Generate `project_blueprint.md` with an exact [X]-page budget matrix, heading decompositions, and `build_report.py`.
3. Present the Phased Implementation Plan for my approval before drafting any sections.
```

# Prompt to give for AI Code Generation



## 1. System Architecture & Core Principles

Scaling AI-generated documentation beyond 10–20 pages cannot be achieved in a single prompt execution loop. Large-document generation requires a **Phased State Machine** adhering to three core principles:

1. **The 6-Layer Deconstruction Standard:** Every component/module must be analyzed across 6 distinct technical depths:
   * *Layer 1:* Theoretical & Mathematical Foundation (Formulas, Big-O complexity, state machines)
   * *Layer 2:* Data Structures & Schemas (SQL DDL, class dataclasses, protocol interfaces)
   * *Layer 3:* Execution Lifecycle & Step-by-Step Flow Control (ASCII sequence/pipeline graphs)
   * *Layer 4:* Configuration Matrices & Tuning Parameters (Tabular configuration specifications)
   * *Layer 5:* Failure Modes, Circuit Breaking & Edge Fallbacks (Error codes, jitter, fast-fails)
   * *Layer 6:* Standard Operating Procedures & Runbooks (Executable CLI/SQL/API scripts)
2. **Iterative Chunking Protocol:** Generating strictly **one section file at a time** behind a human review/approval gate.
3. **Strict Quantitative Budgeting:** Every section is allocated a non-negotiable page and word count budget before writing begins.

---

## 2. Workspace Setup & Directory Structure

Organize your project directory as follows before issuing prompts:

```
project-workspace/
├── README.md                          <-- This guide
├── .antigravity/
│   └── rules.md                       <-- Agent behavioral guardrails & zero-hallucination rules
├── raw_sources/                       <-- Place your input files here
│   ├── source_doc_1.docx              <-- (If generating from existing docs)
│   ├── source_doc_2.docx
│   └── codebase/                      <-- (If generating directly from code repository)
├── report_sections/                   <-- Modular generation target directory
│   ├── 00_front_matter.md
│   ├── section_01_*.md
│   ├── section_02_*.md
│   └── ...
├── project_blueprint.md               <-- Master page budget, TOC, and artifact allocation
└── build_report.py                    <-- Automated Pandoc/OpenXML Word compilation script
```

---

## 3. End-to-End Execution Roadmap & Prompt Sequence

### Step 1: Initialize Workspace & Establish System Directives (`rules.md`)
**User Action:** Upload the input source material (either code repository or `.docx` files) and format specifications (or structural guidelines image).

**Copy-Paste Prompt to Agent:**
```text
Read all provided source materials in `raw_sources/` and the target structural guidelines. 

Your first task is to generate `.antigravity/rules.md` to establish strict operational guardrails. 
The rules.md file must enforce:
1. Zero-Hallucination Policy: All class signatures, API routes, database schemas, and metrics must map directly to the source materials or standard RFC specifications. Placeholders (# TODO, // implement here, ...) are strictly prohibited.
2. Iterative Chunking: You must generate strictly ONE section/heading file per prompt turn and await user approval before proceeding.
3. 6-Layer Deconstruction Standard: Every system module must include mathematical foundations, concrete DDL/schemas, execution lifecycles, configuration matrices, edge cases, and actionable SOP runbooks.
4. Word Budget Compliance: Mandatory target word counts per section to guarantee natural document scaling.
```

---

### Step 2: Generate Master Blueprint & Word-Count Allocation (`project_blueprint.md`)
**Copy-Paste Prompt to Agent:**
```text
Based on our target output of [X] pages (approx. [X * 300] words) and the required structural format:

Generate `project_blueprint.md` containing:
1. Document Front Matter Specifications (Title Page, Institutional Certificates, Declaration, Table of Contents).
2. Master Page & Word Allocation Matrix: A comprehensive table assigning exact page budgets, word budgets, target file names (`report_sections/00_*.md` to `report_sections/XX_*.md`), and mandatory technical artifacts for every single section.
3. Step-by-Step Execution Plan: State machine breakdown from Phase 0 (Pre-flight) to Phase N (Final Pandoc Compilation).
4. Complete `build_report.py` compilation script injecting OpenXML page breaks (`<w:p><w:r><w:br w:type="page"/></w:r></w:p>`) and Pandoc terminal syntax.
```

---

### Step 3: Generate Phased Implementation Plan
**Copy-Paste Prompt to Agent:**
```text
Read and strictly adhere to `.antigravity/rules.md` and `project_blueprint.md`.

Before writing any report Markdown files, generate ONLY the comprehensive IMPLEMENTATION PLAN.
1. Outline the phased order of file generation.
2. List the exact target word count and required concrete artifacts for each file.
3. Confirm that you will proceed strictly one section at a time upon explicit user approval.

Do NOT generate report sections yet. Output only the implementation plan and await confirmation to begin Phase 1.
```

---

### Step 4: Phased Section Generation (Iterative Execution Loop)
**Copy-Paste Prompt Template per Section:**
```text
We are generating Section [File Name, e.g., report_sections/section_01_methodology.md].
Target Budget: [Target Word Count] words across [Target Page Count] pages.

Strictly adhere to .antigravity/rules.md:
- Ground every detail in `raw_sources/`.
- Apply the 6-Layer Engineering layout (Theory, Schemas, Flow, Config Matrix, Edge Cases, SOP Runbooks).
- Output complete, unabbreviated code blocks, database DDL, and runnable CLI scripts.
- Do NOT proceed to the next section upon completion; state that the section is ready for review.
```

---

### Step 5: Automated Compilation to Microsoft Word (`.docx`)
**User Action:** Once all section markdown files are generated in `report_sections/`, execute the compilation pipeline in the workspace terminal:

```bash
# Run automated build script
python build_report.py
```

*Or run Pandoc directly:*
```bash
pandoc report_sections/*.md   -o Final_Technical_Report.docx   --toc   --toc-depth=3   --highlight-style=tango   --variable=geometry:margin=1in
```

---