import os
import argparse
import subprocess
import sys

PAGE_BREAK = "\n\n```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```\n\n"

def build(sections_dir, output_docx, reference_doc=None):
    if not os.path.isdir(sections_dir):
        print(f"[-] Error: Directory '{sections_dir}' does not exist.")
        sys.exit(1)

    # Auto-discover markdown files, sorted alphabetically
    md_files = [f for f in os.listdir(sections_dir) if f.endswith('.md')]
    md_files.sort()

    if not md_files:
        print(f"[-] Error: No markdown files found in '{sections_dir}'.")
        sys.exit(1)

    merged_data = []
    for filename in md_files:
        filepath = os.path.join(sections_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            merged_data.append(f.read().strip())
            merged_data.append(PAGE_BREAK)
    
    # Save merged intermediate file in the same directory as output
    output_dir = os.path.dirname(os.path.abspath(output_docx))
    merged_file = os.path.join(output_dir, "merged_draft.md")
    
    with open(merged_file, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_data))
    
    print(f"[*] Successfully merged {len(md_files)} sections into {merged_file}")

    cmd = [
        "pandoc",
        merged_file,
        "-o",
        output_docx,
        "--toc",
        "--toc-depth=3",
        "--highlight-style=tango",
        "--variable=geometry:margin=1in",
    ]

    if reference_doc and os.path.isfile(reference_doc):
        cmd.extend(["--reference-doc", reference_doc])

    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE, text=True)
        print(f"[+] Document compiled successfully: {output_docx}")
    except subprocess.CalledProcessError as err:
        print(f"[-] Compilation error:")
        print(err.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("[-] Pandoc is not installed or not in PATH. Merged Markdown file is available.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile markdown sections into a .docx using Pandoc.")
    parser.add_argument("--sections-dir", required=True, help="Directory containing markdown sections to merge.")
    parser.add_argument("--output", required=True, help="Output .docx filename.")
    parser.add_argument("--reference-doc", help="Optional Pandoc reference .docx for styling.")
    
    args = parser.parse_args()
    build(args.sections_dir, args.output, args.reference_doc)
