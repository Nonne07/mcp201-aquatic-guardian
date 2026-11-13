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
import re
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

def set_table_borders(table, color="D0D7DE", sz="4", val="single"):
    """Applies clean outer border to a table."""
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideH w:val="none"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def add_page_number(run):
    """Inserts a dynamic page number field into a run."""
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

def add_formula_box(doc, formula_text, eq_number=""):
    """Inserts a dedicated shaded formula box with right-aligned numbering and professional math typography."""
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, color="B0C4DE", sz="6", val="single")

    # Left cell: Math formula (width ~ 13.2 cm)
    cell_form = table.cell(0, 0)
    cell_form.width = Cm(13.2)
    set_cell_background(cell_form, "F4F6F9")
    set_cell_margins(cell_form, top=140, bottom=140, left=180, right=100)
    p_form = cell_form.paragraphs[0]
    p_form.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_form.paragraph_format.space_before = Pt(4)
    p_form.paragraph_format.space_after = Pt(4)

    # Tokenize formula for subscripts, superscripts and regular math symbols
    pattern = re.compile(r'_([a-zA-Z0-9]+|\([^)]+\))|\^([a-zA-Z0-9]+|\([^)]+\))|([^_^\n]+)')
    for m in pattern.finditer(formula_text):
        sub_val = m.group(1)
        sup_val = m.group(2)
        norm_val = m.group(3)
        if sub_val is not None:
            r = p_form.add_run(sub_val.strip('()'))
            r.font.name = 'Cambria Math'
            r.font.size = Pt(11)
            r.font.italic = True
            r.font.subscript = True
            r.font.color.rgb = RGBColor(0, 32, 96)
        elif sup_val is not None:
            r = p_form.add_run(sup_val.strip('()'))
            r.font.name = 'Cambria Math'
            r.font.size = Pt(11)
            r.font.italic = True
            r.font.superscript = True
            r.font.color.rgb = RGBColor(0, 32, 96)
        elif norm_val is not None:
            r = p_form.add_run(norm_val)
            r.font.name = 'Cambria Math'
            r.font.size = Pt(12)
            r.font.italic = True
            r.font.color.rgb = RGBColor(0, 32, 96)

    # Right cell: Equation number (width ~ 2.3 cm)
    cell_num = table.cell(0, 1)
    cell_num.width = Cm(2.3)
    set_cell_background(cell_num, "F4F6F9")
    set_cell_margins(cell_num, top=140, bottom=140, left=50, right=180)
    p_num = cell_num.paragraphs[0]
    p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_num.paragraph_format.space_before = Pt(4)
    p_num.paragraph_format.space_after = Pt(4)
    r_num = p_num.add_run(eq_number)
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(12)
    r_num.font.bold = True
    r_num.font.color.rgb = RGBColor(0, 43, 73)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(6)

def add_callout_box(doc, text_lines):
    """Inserts a styled note / quote callout box."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="002B49"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="none"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

    cell = table.cell(0, 0)
    cell.width = Cm(15.5)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.3
    full_text = " ".join(text_lines)
    format_inline_markdown(p, full_text)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(6)

def add_code_block(doc, code_lines):
    """Inserts a formatted code/ASCII diagram block."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, color="CCD6E0", sz="4", val="single")

    cell = table.cell(0, 0)
    cell.width = Cm(15.5)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=120, bottom=120, left=150, right=150)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05

    for idx, c_line in enumerate(code_lines):
        r = p.add_run(c_line + ("\n" if idx < len(code_lines) - 1 else ""))
        r.font.name = 'Consolas'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(20, 30, 40)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(6)

def clean_latex_artifacts(text):
    """Replaces common LaTeX artifacts with clean Unicode symbols."""
    text = text.replace(r'$NH_3$', 'NH₃')
    text = text.replace(r'$NO_2^-$', 'NO₂⁻')
    text = text.replace(r'$\pm 0.5^\circ\text{C}$', '±0.5°C')
    text = text.replace(r'$\pm 1.5\text{ ppm}$', '±1.5 ppm')
    text = text.replace(r'$\pm 50\text{ ppm}$', '±50 ppm')
    text = text.replace(r'$\pm 65$', '±65')
    text = text.replace(r'$0.25^\circ\text{C}$', '0.25°C')
    text = text.replace(r'$25.0^\circ\text{C}$', '25.0°C')
    text = text.replace(r'$0^\circ \to 90^\circ$', '0° → 90°')
    text = text.replace(r'$0^\circ$', '0°')
    text = text.replace(r'$90^\circ$', '90°')
    text = text.replace(r'$1.0\text{ ms}$', '1.0 ms')
    text = text.replace(r'$1.5\text{ ms}$', '1.5 ms')
    text = text.replace(r'$380\text{ ms}$', '380 ms')
    text = text.replace(r'$800\text{ ms}$', '800 ms')
    text = text.replace(r'$1500\text{ ms}$', '1500 ms')
    text = text.replace(r'$185\text{ ms}$', '185 ms')
    text = text.replace(r'$300\text{ ms}$', '300 ms')
    text = text.replace(r'$4.2\text{ ms}$', '4.2 ms')
    text = text.replace(r'$2.8\text{ ms}$', '2.8 ms')
    text = text.replace(r'$10\text{ ms}$', '10 ms')
    text = text.replace(r'$50\text{ ms}$', '50 ms')
    text = text.replace(r'$1.5\text{ giây}$', '1.5 giây')
    text = text.replace(r'$1\mu\text{s}$', '1 µs')
    text = text.replace(r'$0.85\,\mu\text{s}$', '0.85 µs')
    text = text.replace(r'$10\,\mu\text{s}$', '10 µs')
    text = text.replace(r'$48.2\text{ KB}$', '48.2 KB')
    text = text.replace(r'$512.0\text{ KB}$', '512.0 KB')
    text = text.replace(r'$12.4\text{ KB}$', '12.4 KB')
    text = text.replace(r'$96.0\text{ KB}$', '96.0 KB')
    text = text.replace(r'$4096\text{ Bytes}$', '4096 Bytes')
    text = text.replace(r'$8192\text{ Bytes}$', '8192 Bytes')
    text = text.replace(r'$112.4\text{ ppm}$', '112.4 ppm')
    text = text.replace(r'$685.2\text{ ppm}$', '685.2 ppm')
    text = text.replace(r'$100\%$', '100%')
    text = text.replace(r'$5\text{V} - 3.3\text{V} = 1.7\text{V}$', '5V - 3.3V = 1.7V')
    text = text.replace(r'$O(1)$', 'O(1)')
    text = text.replace(r'$O(N)$', 'O(N)')
    text = text.replace(r'$N = 20$', 'N = 20')
    text = text.replace(r'$\text{CCR1} = 1000$', 'CCR1 = 1000')
    text = text.replace(r'$\text{CCR1} = 1500$', 'CCR1 = 1500')
    text = text.replace(r'$\text{Dwell Time}$', 'Dwell Time')
    text = text.replace(r'$V_{\text{comp}}$', 'V_comp')
    text = text.replace(r'$V_{\text{adc}}$', 'V_adc')
    text = text.replace(r'$T_{\text{water}}$', 'T_water')
    text = text.replace(r'$X_{\text{new}}$', 'X_new')
    text = text.replace(r'$X_{\text{old}}$', 'X_old')
    text = text.replace(r'$X_{\text{filtered}}$', 'X_filtered')
    return text

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

    in_code = False
    code_lines = []

    in_quote = False
    quote_lines = []
    
    for line in lines:
        raw = line.rstrip('\r\n')
        stripped = raw.strip()

        # Handle Code block delimiters (```)
        if stripped.startswith('```'):
            if in_code:
                in_code = False
                add_code_block(doc, code_lines)
                code_lines = []
            else:
                in_code = True
                code_lines = []
            continue

        if in_code:
            code_lines.append(raw)
            continue

        # Handle Blockquotes (starts with >)
        if stripped.startswith('>'):
            in_quote = True
            quote_text = stripped[1:].strip()
            if quote_text:
                quote_lines.append(quote_text)
            continue
        elif in_quote:
            in_quote = False
            add_callout_box(doc, quote_lines)
            quote_lines = []

        # Handle Dedicated Formula Lines (delimited by $$ ... $$)
        if stripped.startswith('$$') and stripped.endswith('$$'):
            content = stripped[2:-2].strip()
            # Extract trailing equation tag like (2.1), (3.1), etc.
            eq_match = re.search(r'\(([0-9]+\.[0-9]+)\)\s*$', content)
            if eq_match:
                eq_num = f"({eq_match.group(1)})"
                formula_text = content[:eq_match.start()].strip()
            else:
                eq_num = ""
                formula_text = content
            add_formula_box(doc, formula_text, eq_num)
            continue

        # Handle markdown table blocks
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table:
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
            text = clean_latex_artifacts(stripped[2:].strip())
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            format_inline_markdown(p, text)

        # Numbered items
        elif len(stripped) > 2 and stripped[0].isdigit() and stripped[1] in ['.', ')']:
            text = clean_latex_artifacts(stripped[2:].strip())
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            format_inline_markdown(p, text)

        # Standard Paragraphs
        else:
            text = clean_latex_artifacts(stripped)
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            format_inline_markdown(p, text)

    # Flush any trailing table, quote, or code
    if in_table and table_lines:
        process_markdown_table(doc, table_lines)
    if in_code and code_lines:
        add_code_block(doc, code_lines)
    if in_quote and quote_lines:
        add_callout_box(doc, quote_lines)

    out_docx = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\BAO_CAO_DO_AN_AQUATIC_GUARDIAN.docx"
    try:
        doc.save(out_docx)
        print(f"[SUCCESS] High-fidelity academic report saved to: {out_docx}")
    except PermissionError:
        alt_docx = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\BAO_CAO_DO_AN_AQUATIC_GUARDIAN_v2.docx"
        doc.save(alt_docx)
        print(f"[WARNING] '{out_docx}' is currently locked by Microsoft Word. Successfully saved updated report to: {alt_docx}")

def format_inline_markdown(p, text):
    """Parses bold, italic, and code spans in paragraph text."""
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
        cols = [clean_latex_artifacts(c.strip()) for c in l.split('|')[1:-1]]
        if cols:
            rows_data.append(cols)

    if not rows_data:
        return

    num_rows = len(rows_data)
    num_cols = max(len(r) for r in rows_data)

    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    set_table_borders(table, color="D0D7DE", sz="4", val="single")

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
