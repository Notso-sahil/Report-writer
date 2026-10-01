import re

def update():
    with open("build_report.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update add_declaration
    old_decl = """def add_declaration(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("DECLARATION")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True"""
    new_decl = """def add_declaration(doc):
    p = doc.add_paragraph(style='Heading 1')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("DECLARATION")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.paragraph_format.space_before = Pt(0)"""
    content = content.replace(old_decl, new_decl)

    # 2. Update add_image_page (Offer letter, certificate, employer feedback)
    old_img = """def add_image_page(doc, title, image_path):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True"""
    new_img = """def add_image_page(doc, title, image_path):
    p = doc.add_paragraph(style='Heading 1')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    p.paragraph_format.space_before = Pt(0)"""
    content = content.replace(old_img, new_img)

    # 3. Update add_acknowledgement
    old_ack = """    for _ in range(2): doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("ACKNOWLEDGEMENT")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    for _ in range(4): doc.add_paragraph()"""
    new_ack = """    p = doc.add_paragraph(style='Heading 1')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(80)
    p.paragraph_format.space_after = Pt(72)
    run = p.add_run("ACKNOWLEDGEMENT")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)"""
    content = content.replace(old_ack, new_ack)

    # 4. Update the save path to Final_Report_v4.docx
    content = content.replace('output_path = "Final_Report_v3.docx"', 'output_path = "Final_Report_v4.docx"')

    with open("build_report.py", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update()
