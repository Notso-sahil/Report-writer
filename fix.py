import os
import re

def rewrite_build_report():
    with open("build_report.py", "r", encoding="utf-8") as f:
        content = f.read()
        
    new_inline_formatter = """def _parse_inline_formatting(paragraph, text):
    parts = re.split(r'(\*\*.*?\*\*|`.*?`)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.font.bold = True
            run.font.name = 'Times New Roman'
        elif part.startswith('`') and part.endswith('`'):
            run = paragraph.add_run(part[1:-1])
            run.font.name = 'Courier New'
        else:
            run = paragraph.add_run(part)
            run.font.name = 'Times New Roman'
    for run in paragraph.runs:
        if run.font.name != 'Courier New':
            run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
"""

    new_parser = """def get_blocks(lines):
    blocks = []
    current_block = []
    block_type = "TEXT"
    in_code = False
    
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith('```'):
            if current_block:
                blocks.append((block_type, current_block))
                current_block = []
            in_code = not in_code
            block_type = "CODE" if in_code else "TEXT"
            continue
            
        if in_code:
            current_block.append(line)
            continue
            
        if not stripped:
            if current_block:
                blocks.append((block_type, current_block))
                current_block = []
            continue
            
        is_new_block = (
            stripped.startswith('#') or 
            stripped.startswith('![') or 
            stripped.startswith('|') or
            stripped == '<!-- -->' or
            re.match(r'^[\-\*]\s', stripped) or
            re.match(r'^\d+\.\s', stripped) or
            stripped.startswith('> ')
        )
        
        if is_new_block:
            if current_block:
                blocks.append((block_type, current_block))
                current_block = []
            block_type = "TABLE" if stripped.startswith('|') else "TEXT"
            current_block.append(stripped)
        else:
            if block_type == "TABLE" and not stripped.startswith('|'):
                blocks.append((block_type, current_block))
                current_block = [stripped]
                block_type = "TEXT"
            else:
                if block_type == "TEXT":
                    current_block.append(stripped)
                else:
                    current_block.append(stripped)
                    
    if current_block:
        blocks.append((block_type, current_block))
        
    return blocks

def parse_markdown_to_docx(doc, md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    lines = md_text.split('\\n')
    blocks = get_blocks(lines)
    
    chapter_count = 0
    
    try:
        caption_style = doc.styles['Caption']
    except KeyError:
        caption_style = doc.styles.add_style('Caption', WD_STYLE_TYPE.PARAGRAPH)
    caption_style.font.name = 'Times New Roman'
    caption_style.font.size = Pt(12)
    caption_style.font.bold = True
    caption_style.font.color.rgb = RGBColor(0,0,0)

    for btype, block_lines in blocks:
        if btype == "CODE":
            p = doc.add_paragraph('\\n'.join(block_lines))
            p.style = doc.styles['No Spacing']
            p.paragraph_format.left_indent = Cm(1)
            for run in p.runs:
                run.font.name = 'Courier New'
                run.font.size = Pt(10)
            doc.add_paragraph()
            continue
            
        if btype == "TABLE":
            table_data = []
            for line in block_lines:
                if re.match(r'^\|[\s\-\|]+\|$', line):
                    continue
                cols = [col.strip() for col in line.strip('|').split('|')]
                table_data.append(cols)
                
            if table_data:
                p_cap = doc.add_paragraph(style='Caption')
                p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run_cap = p_cap.add_run("Table ")
                add_seq_field(run_cap, "Table")
                p_cap.add_run(": Data Table")
                p_cap.paragraph_format.space_after = Pt(6)
                
                table = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
                table.style = 'Table Grid'
                for r_idx, row in enumerate(table_data):
                    for c_idx, cell_text in enumerate(row):
                        cell = table.cell(r_idx, c_idx)
                        cell.text = cell_text
                        for paragraph in cell.paragraphs:
                            for run in paragraph.runs:
                                run.font.name = 'Times New Roman'
                                run.font.size = Pt(11)
                doc.add_paragraph()
            continue
            
        # It's TEXT. Join lines to form a single paragraph (resolves hard wrapping)
        text = " ".join(block_lines).strip()
        
        if chapter_count == 0 and not text.startswith('# '):
            continue
            
        img_match = re.match(r'^!\[(.*?)\]\((.*?)\)', text)
        if img_match:
            caption_text = img_match.group(1)
            img_path = img_match.group(2)
            if os.path.exists(img_path):
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.add_run().add_picture(img_path, width=Cm(14))
            else:
                p = doc.add_paragraph(f"[Image missing: {img_path}]")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
            p_cap = doc.add_paragraph(style='Caption')
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run_cap = p_cap.add_run("Figure ")
            add_seq_field(run_cap, "Figure")
            p_cap.add_run(f": {caption_text}")
            p_cap.paragraph_format.space_before = Pt(6)
            p_cap.paragraph_format.space_after = Pt(12)
            continue
            
        if text.startswith('#'):
            level = len(text) - len(text.lstrip('#'))
            header_text = text.lstrip('#').strip()
            
            is_reference = 'reference' in header_text.lower() or 'appendix' in header_text.lower()
            
            if level == 1 or is_reference:
                if is_reference:
                    level = 1
                    doc.add_page_break()
                    header_text = "References" if 'reference' in header_text.lower() else "Appendix"
                else:
                    chapter_count += 1
                    is_first = (chapter_count == 1)
                    start_chapter(doc, is_first)
                    header_text = f"Chapter-{chapter_count}. {header_text}"
                
            p = doc.add_paragraph(style=f'Heading {level}')
            run = p.add_run(header_text)
            run.font.name = 'Times New Roman'
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
            if level == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.font.size = Pt(16)
            elif level == 2:
                run.font.size = Pt(14)
            else:
                run.font.size = Pt(12)
            p.paragraph_format.space_after = Pt(12)
            continue
            
        num_match = re.match(r'^(\d+)\.\s(.*)', text)
        if num_match:
            list_text = num_match.group(2)
            p = doc.add_paragraph(style='List Number')
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            _parse_inline_formatting(p, list_text)
            continue
            
        if text.startswith('- ') or text.startswith('* '):
            list_text = text[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            _parse_inline_formatting(p, list_text)
            continue
            
        if text.startswith('> '):
            quote_text = text[2:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(1)
            _parse_inline_formatting(p, quote_text)
            continue
            
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        _parse_inline_formatting(p, text)
"""

    import re
    # We replace from def _parse_inline_formatting up to def generate_report()
    content = re.sub(r'def _parse_inline_formatting.*?def generate_report', new_inline_formatter + '\\n' + new_parser + '\\ndef generate_report', content, flags=re.DOTALL)
    
    with open("build_report.py", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    rewrite_build_report()
