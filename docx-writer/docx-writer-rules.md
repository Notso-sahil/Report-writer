---
name: docx-generation-rules
description: >-
  Rules for generating high-quality .docx reports and documents.
trigger: model_decision
---

# Document Generation Rules

Whenever you are tasked with generating a large report, document, or `.docx` file, you MUST strictly adhere to the following Phased Execution Protocol. **Generating the entire document in a single response turn is strictly prohibited** as it leads to context window truncation, shallow summaries, and poor formatting.

## Phased Execution Protocol

### Phase 0: Pre-Flight Verification
- Verify the dependencies and environment setup (ensure Pandoc is installed if required).
- Do not begin writing any content yet.

### Phase 1: Blueprint Generation
- You must create a section-by-section execution checklist or blueprint outlining exactly what each section of the document will contain and its target word budget.
- Present the plan/outline to the user and pause for user approval before proceeding to Phase 2.

### Phase 2: Sequential Section Expansion
- Generate **strictly ONE section or heading per response turn**.
- Fulfill word budgets and include high-quality technical artifacts (e.g., tables, code blocks, GitHub-style alerts like `> [!NOTE]`) per file.
- Save each section as a separate markdown file (e.g., `report_sections/section_01.md`).
- If the user requests the document to be **human-generated, natural, or plagiarism-free**, strictly enforce the **Human-Generated & Plagiarism-Free Protocol** below.
- Draft sections interactively, pausing for user review and approval after each section before continuing.
- Once all sections defined in the blueprint are complete, immediately proceed to Phase 3 (Master Compilation).

### Phase 3: Master Compilation & Zero Workspace Clutter
- Once all sections are written, execute the compilation script directly from the global skill directory (`C:\Users\elite\.gemini\config\skills\docx-writer\scripts\build_docx.py`) or run it from Antigravity's artifact scratch directory.
- **NEVER save one-off compilation scripts (such as `build_report.py` or `build_docx.py`) into the user's project workspace.** The workspace must strictly contain only the document source files and the final output `.docx`.
- The compilation script merges individual markdown files, inserts proper page breaks between sections, and compiles the merged document into the final `.docx` file using Pandoc.

## Human-Generated & Plagiarism-Free Protocol

When the user specifies that the document must be **fully human-generated, natural, bypass AI detection, or plagiarism-free**, you MUST strictly adhere to the following stylistic and structural rules across every section:

1. **START WITH THE POINT**: Skip generic introductions, meta-commentary, rhetorical questions, and warm-up throat-clearing. Open directly with substantive information, findings, or core technical facts.
2. **CUT FILLER & REPETITION**: Every sentence must deliver fresh meaning, context, or technical substance. Ruthlessly eliminate redundancy, self-evident statements, restatements of earlier paragraphs, and circular summaries.
3. **BE CONCRETE & SPECIFIC**: Replace abstract, vague assertions with concrete names, file paths, versions, dates, metrics, parameters, and observed results. Real people write about tangible things.
4. **STAY ACCURATE (ZERO HALLUCINATION)**: Never fabricate facts, statistics, quotes, sources, URLs, CVE numbers, commit hashes, or names. If uncertain or if data is absent, state the limitation plainly rather than inventing plausible-sounding filler.
5. **USE CLEAR LANGUAGE & PRECISE DOMAIN TERMINOLOGY**: Prefer everyday words and strong verbs over pompous academic phrasing. Keep technical domain terms exact (e.g., "smali bytecode", "SHA-256", "mutex lock"), but strictly eliminate empty corporate jargon and notorious AI clichés:
   - **Banned AI words**: *delve, robust, pivotal, transformative, cutting-edge, showcasing, underscoring, testament to, tapestry, beacon, plethora, multifaceted, paramount, foster, elevate, seamless, seamlessly, harnessing, intertwined, game-changer*.
   - **Banned boilerplate formulas**: *"it is worth noting that"*, *"in today's rapidly evolving landscape"*, *"serves as a testament/reminder"*, *"not only X, but also Y"*.
6. **WRITE NATURALLY WITH HIGH BURSTINESS**: AI writing suffers from uniform syntactic cadence and predictable word choices. Mix very short, punchy statements (3–6 words) with varied medium and longer compound sentences. Vary sentence openings and avoid repetitive rhythmic formulas.
7. **AVOID OVER-STRUCTURING & FORCED LISTS**: Do not turn every concept into bullet points with bold lead-ins (`* **Point**: explanation`). Write continuous, analytical paragraphs with natural flow. Reserve lists and tables strictly for actual data sets, discrete specifications, or sequential procedures where formatting genuinely aids comprehension.
8. **NATURAL PUNCTUATION (NO EM DASHES)**: **Never use em dashes (`—`)**, as they are one of the most common statistical markers used by AI detection algorithms. Avoid exclamation marks and excessive rhetorical punctuation. Use standard commas, periods, and occasional parentheses naturally.
9. **SYNTHESIS OVER PLAGIARISM**: Never copy-paste blocks of source text or do superficial synonym-swapping. Internalize the mechanism, concept, or data, and explain it from first principles in an authentic analytical voice. Attribute specific quotes, standards, and external findings with explicit citations.
10. **MATCH THE DOCUMENT CONTEXT**:
    - **Technical reports & dossiers**: Rigorous, direct, evidence-based, and devoid of marketing hype.
    - **Executive briefings**: Crisp, bottom-line focused, quantifying impact, cost, and risk.
    - **Academic/analytical papers**: Nuanced, methodological, highlighting constraints and empirical evidence.
11. **STOP WHEN THE POINT IS COMPLETE**: Never append generic conclusions, predictions, preachy life lessons, or moralizing summaries (*"In conclusion, by embracing X, stakeholders can pave the way..."*). When the analysis or objective is met, stop immediately.
12. **SILENT SELF-EDIT BEFORE GENERATING**: Before outputting any section, silently remove filler, repetition, vague claims, inflated adjectives, awkward phrasing, and lingering AI formulas.

## Quality Standards
- Ensure all technical documentation has extreme depth and clarity.
- Do not use placeholders like `// TODO: implement this`.
- Use Markdown formatting cleanly: bold text where helpful, tables for tabular data, and syntax-highlighted code blocks.
- Ensure the final output matches the requested style or the Pandoc default style if none is specified.
