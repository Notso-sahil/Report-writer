---
name: docx-writer
description: >-
  Use this skill whenever the user asks you to write a report, generate a document, document a codebase, or create a .docx file. It provides a standardized, phased workflow for producing high-quality, large-scale .docx files from markdown sections with support for human-like, plagiarism-free writing.
---

# `docx-writer` Skill

This skill teaches you how to generate professional, high-quality `.docx` files by adhering to a phased, iterative workflow.

## Overview of the Workflow

To produce high-quality documents that do not succumb to context window truncation, you must **never generate an entire document in a single turn**. Instead, you must generate the document section-by-section.

## Phase 0: Check Dependencies
Before writing anything, you must ensure the required tools (`pandoc` and `python-docx`) are installed.
1. Run the dependency checker script:
   `[check_dependencies.ps1](./scripts/check_dependencies.ps1)`
2. If the script reports that any dependencies are missing, **STOP** and ask the user for permission to install them automatically (e.g., via `winget` or `pip`). Wait for their approval before proceeding.

## Phase 1: Blueprint Generation
1. Gather source materials. If the user provided raw `.docx` files as source material, extract their text using:
   `[extract_docx_text.py](./scripts/extract_docx_text.py)`
2. If the user wants a codebase documented, use your search tools to explore the workspace.
3. Generate a Markdown artifact detailing the structure of the document (a blueprint). Use `[blueprint_template.md](./examples/blueprint_template.md)` as a structural guide.
4. Set `RequestFeedback: true` on the blueprint artifact and **STOP**. Ask the user to approve the blueprint before you begin writing.

## Phase 2: Iterative Section Writing
Once the blueprint is approved, you must write the document **one section per turn**.
1. Write the first section to a file in a dedicated directory (e.g., `report_sections/01_intro.md`).
2. Ensure the content is extremely detailed, high-quality, and uses rich Markdown (tables, code blocks, GitHub alerts).
3. If the user requests the document to be **human-generated, natural, or plagiarism-free**, follow the **Human-Generated & Plagiarism-Free Writing Protocol** below.
4. Update your task list.
5. **STOP** and ask the user to click a 'Proceed' button to move to the next section.\n6. Repeat this process until all sections are written.

### Human-Generated & Plagiarism-Free Writing Protocol
When requested to write naturally, bypass AI detection, or ensure zero plagiarism:
- **Start With The Point**: Begin directly with technical or factual data. Skip generic intros and meta-commentary.
- **Cut Filler & Redundancy**: Ensure every sentence adds distinct meaning. No repeating points in slightly different words.
- **High Specificity**: Use exact filenames, commit hashes, CVEs, dates, metrics, parameters, and results.
- **Strict Accuracy**: Zero hallucinations. Never invent statistics, quotes, or sources. State unknowns or limitations directly.
- **Purge AI Clichés & Buzzwords**:
  - *Forbidden vocabulary*: delve, robust, pivotal, transformative, cutting-edge, showcasing, underscoring, testament to, tapestry, beacon, plethora, multifaceted, paramount, foster, elevate, seamless/seamlessly, harnessing, intertwined, game-changer.
  - *Forbidden boilerplate*: "it is worth noting that", "in today's rapidly evolving landscape", "serves as a reminder", "not only X, but also Y".
- **Burstiness & Sentence Variation**: Alternate between punchy short sentences (3–6 words) and longer, multi-clause explanations. Avoid rhythmic uniformity.
- **Avoid Over-Structuring**: Write flowing, cohesive paragraphs. Do not force every concept into bold-prefixed bullet points. Use lists/tables only for genuinely structured items.
- **No Em Dashes**: Never use em dashes (`—`). Use standard commas, periods, and parentheses.
- **Deep Synthesis Over Plagiarism**: Never copy-paste or synonym-swap. Understand concepts from first principles and synthesize them in your own voice. Attribute external facts with explicit citations.
- **Context Register**: Match the document type (technical dossier, executive summary, whitepaper) without artificial corporate hype.
- **Stop When Done**: Do not write moralizing summaries, unsolicited advice, or generic concluding paragraphs. End directly when the objective is met.
- **Pre-Output Silent Edit**: Review the draft to strip filler, repetitive ideas, and AI markers before outputting.

## Phase 3: Document Compilation
Once all sections are written, you will compile them into a single `.docx` file.
1. Execute the compilation script:
   `[build_docx.py](./scripts/build_docx.py)`
   Run it as: `python path/to/build_docx.py --sections-dir ./report_sections --output Final_Report.docx`
2. This script will concatenate the files in alphabetical order, insert OpenXML page breaks, and invoke Pandoc.

## Phase 4: Word Count Verification
1. Verify the final word count of the merged markdown file using:
   `[count_words.ps1](./scripts/count_words.ps1)`
2. Present the final `.docx` file path and the total word count to the user in your final summary.
