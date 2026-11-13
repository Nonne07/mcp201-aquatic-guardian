"""
=============================================================================
Project: Aquatic Guardian - Capstone MCP201
Script: generate_docx_report.py
Purpose: Generates the official Microsoft Word report (.docx) complying
         strictly with '20141225-Huong dan trinh bay DATN.doc'
         and the instructor's reminder ('Lam tu muc luc tro xuong thoi').
=============================================================================
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets padding/margins inside a table cell (values in twips)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_page_number(run):
    """Inserts a dynamic page number field into a run."""
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

def build_report():
    doc = Document()

    # Configure A4 Page Margins as per guidelines
    # Margins: Left=3.0cm, Right=2.5cm, Top=2.5cm, Bottom=3.0cm
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(3.0)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.5)

    # Configure footer page numbering (Bottom, Center)
    footer = section.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_run = f_p.add_run()
    f_run.font.name = 'Times New Roman'
    f_run.font.size = Pt(11)
    add_page_number(f_run)

    # Set base Normal Style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(13)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_before = Pt(6)
    style_normal.paragraph_format.space_after = Pt(4)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Read the master markdown content
    md_path = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\BAO_CAO_DO_AN_AQUATIC_GUARDIAN.md"
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_table = False
    table_lines = []
    
    for line in lines:
        raw = line.rstrip('\r\n')
        stripped = raw.strip()

        # Handle markdown table blocks
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table:
            # End of table, process buffered table
            in_table = False
            process_markdown_table(doc, table_lines)
            table_lines = []

        if not stripped:
            continue

        if stripped == '---':
            continue

        # Heading 1: Chapters & Front Matter (# Title)
        if raw.startswith('# '):
            text = raw[2:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if any(k in text for k in ['MỤC LỤC', 'DANH MỤC', 'TÀI LIỆU', 'PHỤ LỤC']) else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(16)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 43, 73) # ST Navy

        # Heading 2: Level 1 Sections (## 1.1 ...)
        elif raw.startswith('## '):
            text = raw[3:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Heading 3: Level 2 Subsections (### 1.1.1 ...)
        elif raw.startswith('### '):
            text = raw[4:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Table Captions (starts with *Bảng...)
        elif stripped.startswith('*Bảng ') or stripped.startswith('Bảng '):
            clean_text = stripped.replace('*', '')
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(clean_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(13)
            run.font.bold = True

        # Figure Captions (starts with *Hình...)
        elif stripped.startswith('*Hình ') or stripped.startswith('Hình '):
            clean_text = stripped.replace('*', '')
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(14)
            run = p.add_run(clean_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
            run.font.italic = True

        # Bullet items
        elif stripped.startswith('* ') or stripped.startswith('- '):
            text = stripped[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            format_inline_markdown(p, text)

        # Numbered items
        elif len(stripped) > 2 and stripped[0].isdigit() and stripped[1] in ['.', ')']:
            text = stripped[2:].strip()
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            format_inline_markdown(p, text)

        # Standard Paragraphs
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            format_inline_markdown(p, stripped)

    # If any trailing table
    if in_table and table_lines:
        process_markdown_table(doc, table_lines)

    out_docx = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\BAO_CAO_DO_AN_AQUATIC_GUARDIAN.docx"
    doc.save(out_docx)
    print(f"[SUCCESS] Report saved to: {out_docx}")

def format_inline_markdown(p, text):
    """Parses bold, italic, and code spans in paragraph text."""
    # Simple parser for **bold** and *italic*
    parts = text.split('**')
    for i, part in enumerate(parts):
        if not part:
            continue
        is_bold = (i % 2 == 1)
        subparts = part.split('*')
        for j, subpart in enumerate(subparts):
            if not subpart:
                continue
            is_italic = (j % 2 == 1)
            # handle `code`
            code_parts = subpart.split('`')
            for k, cpart in enumerate(code_parts):
                if not cpart:
                    continue
                is_code = (k % 2 == 1)
                run = p.add_run(cpart)
                run.font.name = 'Consolas' if is_code else 'Times New Roman'
                run.font.size = Pt(11.5) if is_code else Pt(13)
                run.font.bold = is_bold
                run.font.italic = is_italic
                if is_code:
                    run.font.color.rgb = RGBColor(160, 40, 40)

def process_markdown_table(doc, lines):
    """Converts markdown table lines into a styled Word table."""
    rows_data = []
    for l in lines:
        if '---' in l:
            continue # Skip markdown separator row
        cols = [c.strip() for c in l.split('|')[1:-1]]
        if cols:
            rows_data.append(cols)

    if not rows_data:
        return

    num_rows = len(rows_data)
    num_cols = max(len(r) for r in rows_data)

    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    # Style header row
    for col_idx, text in enumerate(rows_data[0]):
        cell = table.cell(0, col_idx)
        set_cell_background(cell, "002B49") # Dark Navy
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text.replace('**', ''))
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)

    # Style data rows
    for row_idx in range(1, num_rows):
        r_data = rows_data[row_idx]
        is_even = (row_idx % 2 == 0)
        for col_idx in range(num_cols):
            cell = table.cell(row_idx, col_idx)
            val = r_data[col_idx] if col_idx < len(r_data) else ""
            if is_even:
                set_cell_background(cell, "F2F5F8") # Subtle zebra stripe
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 2, 3] and len(val) < 20 else WD_ALIGN_PARAGRAPH.LEFT
            format_inline_markdown(p, val)
            for r in p.runs:
                r.font.size = Pt(11)

    # Add spacing after table
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(8)

if __name__ == '__main__':
    build_report()
