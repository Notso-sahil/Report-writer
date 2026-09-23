import os
import subprocess
import sys

SECTIONS_DIR = "report_sections"
PAGE_BREAK = "\n\n```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```\n\n"
MERGED_FILE = "merged_draft.md"
OUTPUT_DOCX = "Final_Report.docx"

def build():
    if not os.path.exists(SECTIONS_DIR):
        print(f"[-] Error: Directory '{SECTIONS_DIR}' does not exist.")
        sys.exit(1)

    md_files = [f for f in os.listdir(SECTIONS_DIR) if f.endswith(".md")]
    md_files.sort()

    if not md_files:
        print(f"[-] Error: No markdown files found in '{SECTIONS_DIR}'.")
        sys.exit(1)

    merged_data = []
    for filename in md_files:
        filepath = os.path.join(SECTIONS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            merged_data.append(f.read().strip())
            merged_data.append(PAGE_BREAK)

    with open(MERGED_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_data))
    
    print(f"[*] Successfully merged {len(md_files)} sections into {MERGED_FILE}")

    cmd = [
        "pandoc",
        MERGED_FILE,
        "-o",
        OUTPUT_DOCX,
        "--toc",
        "--toc-depth=3",
        "--highlight-style=tango",
        "--variable=geometry:margin=1in",
    ]
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE, text=True)
        print(f"[+] Document compiled successfully: {OUTPUT_DOCX}")
    except subprocess.CalledProcessError as err:
        print(f"[-] Compilation error:")
        print(err.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("[-] Pandoc is not installed or not in PATH. Merged Markdown file is available.")

if __name__ == "__main__":
    build()
