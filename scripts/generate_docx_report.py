"""
=============================================================================
Project: Aquatic Guardian - Capstone MCP201
Script: generate_docx_report.py
Purpose: Generates the official, publication-grade academic report (.docx)
         with a complete formal structure (Outer Cover, Inner Cover,
         Assignment Sheet, Project Rubric, Declaration, Acknowledgments,
         Abstract, Table of Contents, Chapters 1-5, References, Appendices,
         and Teacher Review Sheet) and exports it directly to PDF.
Style:   Professional Monochrome Academic Design for Thesis Printing
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

def set_table_borders(table, color="808080", sz="4", val="single"):
    """Applies subtle monochrome borders to a table."""
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def add_page_number(run):
    """Inserts a dynamic page number field into a run."""
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

def add_hyperlink(paragraph, url, text, is_code=False, is_bold=False):
    """Inserts a clickable Word hyperlink in black text with clean underline."""
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink = parse_xml(f'<w:hyperlink {nsdecls("w", "r")} r:id="{r_id}" w:history="1"/>')
    
    font_name = 'Consolas' if is_code else 'Times New Roman'
    sz_val = "23" if is_code else "26"
    bold_tag = '<w:b/>' if is_bold else ''
    
    r_xml = (
        f'<w:r {nsdecls("w")}>'
        f'  <w:rPr>'
        f'    <w:rFonts w:ascii="{font_name}" w:hAnsi="{font_name}"/>'
        f'    <w:sz w:val="{sz_val}"/>'
        f'    <w:color w:val="000000"/>'
        f'    <w:u w:val="single"/>'
        f'    {bold_tag}'
        f'  </w:rPr>'
        f'  <w:t>{text}</w:t>'
        f'</w:r>'
    )
    r = parse_xml(r_xml)
    hyperlink.append(r)
    paragraph._p.append(hyperlink)

def add_formula_box(doc, formula_text, eq_number=""):
    """Inserts a dedicated formula box with right-aligned numbering and monochrome typography."""
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, color="707070", sz="4", val="single")

    cell_form = table.cell(0, 0)
    cell_form.width = Cm(13.2)
    set_cell_background(cell_form, "FAFAFA")
    set_cell_margins(cell_form, top=130, bottom=130, left=180, right=100)
    p_form = cell_form.paragraphs[0]
    p_form.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_form.paragraph_format.space_before = Pt(3)
    p_form.paragraph_format.space_after = Pt(3)

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
            r.font.color.rgb = RGBColor(0, 0, 0)
        elif sup_val is not None:
            r = p_form.add_run(sup_val.strip('()'))
            r.font.name = 'Cambria Math'
            r.font.size = Pt(11)
            r.font.italic = True
            r.font.superscript = True
            r.font.color.rgb = RGBColor(0, 0, 0)
        elif norm_val is not None:
            r = p_form.add_run(norm_val)
            r.font.name = 'Cambria Math'
            r.font.size = Pt(12)
            r.font.italic = True
            r.font.color.rgb = RGBColor(0, 0, 0)

    cell_num = table.cell(0, 1)
    cell_num.width = Cm(2.3)
    set_cell_background(cell_num, "FAFAFA")
    set_cell_margins(cell_num, top=130, bottom=130, left=50, right=180)
    p_num = cell_num.paragraphs[0]
    p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_num.paragraph_format.space_before = Pt(3)
    p_num.paragraph_format.space_after = Pt(3)
    r_num = p_num.add_run(eq_number)
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(12)
    r_num.font.bold = True
    r_num.font.color.rgb = RGBColor(0, 0, 0)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(6)

def add_callout_box(doc, text_lines):
    """Inserts a styled note / quote callout box in clean monochrome style."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="000000"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="none"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

    cell = table.cell(0, 0)
    cell.width = Cm(15.5)
    set_cell_background(cell, "F7F7F7")
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
    """Inserts a formatted code/ASCII diagram block in neutral monochrome style."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, color="808080", sz="4", val="single")

    cell = table.cell(0, 0)
    cell.width = Cm(15.5)
    set_cell_background(cell, "FAFAFA")
    set_cell_margins(cell, top=120, bottom=120, left=150, right=150)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05

    for idx, c_line in enumerate(code_lines):
        r = p.add_run(c_line + ("\n" if idx < len(code_lines) - 1 else ""))
        r.font.name = 'Consolas'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0, 0, 0)

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

def add_front_cover_page(doc):
    """Builds the formal Outer Cover Page with academic double border."""
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.5)

    # Double border frame on Cover Section
    pgBorders = parse_xml(
        f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">\n'
        f'  <w:top w:val="double" w:sz="12" w:space="24" w:color="000000"/>\n'
        f'  <w:left w:val="double" w:sz="12" w:space="24" w:color="000000"/>\n'
        f'  <w:bottom w:val="double" w:sz="12" w:space="24" w:color="000000"/>\n'
        f'  <w:right w:val="double" w:sz="12" w:space="24" w:color="000000"/>\n'
        f'</w:pgBorders>'
    )
    sec._sectPr.append(pgBorders)

    # Header University Info
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC FPT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run("KHOA VI MẠCH BÁN DẪN & Ô TÔ SỐ\n-----------------------***-----------------------")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    # Report Category
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(36)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("BÁO CÁO ĐỒ ÁN TỐT NGHIỆP HỌC PHẦN\nLẬP TRÌNH VI ĐIỀU KHIỂN (MCP201)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True

    # Project Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(32)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run("ĐỀ TÀI:")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("AQUATIC GUARDIAN")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(24)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(40)
    r = p.add_run("HỆ THỐNG NHÚNG THÔNG MINH GIÁM SÁT CHẤT LƯỢNG NƯỚC\nVÀ CHO ĂN TỰ ĐỘNG THỜI GIAN THỰC")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    # Student Info Header
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.left_indent = Cm(2.2)
    p.paragraph_format.space_before = Pt(40)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("SINH VIÊN THỰC HIỆN:    LỚP IC2005 — NHÓM 7")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True

    team_members = [
        ("1.  Nghiêm Hoàng Tùng", "MSSV: SE211196", "(Trưởng nhóm)"),
        ("2.  Hoàng Đức Mạnh", "MSSV: SE211191", "(Thành viên)"),
        ("3.  Đỗ Khắc Lê Gia", "MSSV: SE211559", "(Thành viên)"),
        ("4.  Phạm Hồng Minh", "MSSV: SE211181", "(Thành viên)"),
        ("5.  Nguyễn Đức Anh", "MSSV: SE211485", "(Thành viên)")
    ]

    table_team = doc.add_table(rows=5, cols=3)
    table_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_team.autofit = False

    tblPr = table_team._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'  <w:insideH w:val="none"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

    # Indent table 2.2 cm from left margin to align with header
    tblInd = parse_xml(f'<w:tblInd {nsdecls("w")} w:w="1247" w:type="dxa"/>')
    tblPr.append(tblInd)

    col_widths = [Cm(6.0), Cm(4.0), Cm(3.2)]
    for r_idx, (m_name, m_mssv, m_role) in enumerate(team_members):
        row = table_team.rows[r_idx]
        for c_idx, val in enumerate([m_name, m_mssv, m_role]):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            set_cell_margins(cell, top=35, bottom=35, left=40, right=40)
            p_cell = cell.paragraphs[0]
            p_cell.paragraph_format.space_before = Pt(0)
            p_cell.paragraph_format.space_after = Pt(0)
            p_cell.paragraph_format.line_spacing = 1.2
            p_cell.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r_c = p_cell.add_run(val)
            r_c.font.name = 'Times New Roman'
            r_c.font.size = Pt(12.5)

def add_assignment_and_rubric_page(doc):
    """Builds the official Project Assignment & Assessment Rubric page."""
    # Add Section 2 for Front Matter (Roman numerals i, ii, iii...)
    sec2 = doc.add_section()
    sec2.footer.is_linked_to_previous = False
    sec2.top_margin = Cm(2.5)
    sec2.bottom_margin = Cm(2.5)
    sec2.left_margin = Cm(3.0)
    sec2.right_margin = Cm(2.5)
    sectPr2 = sec2._sectPr
    pgNumType2 = parse_xml(f'<w:pgNumType {nsdecls("w")} w:start="1" w:fmt="lowerRoman"/>')
    sectPr2.append(pgNumType2)

    footer = sec2.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_run = f_p.add_run()
    f_run.font.name = 'Times New Roman'
    f_run.font.size = Pt(11)
    add_page_number(f_run)

    # Heading
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("PHIẾU GIAO NHIỆM VỤ ĐỒ ÁN VÀ ĐÁNH GIÁ KẾT QUẢ")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("HỌC PHẦN: LẬP TRÌNH VI ĐIỀU KHIỂN (MCP201) — HỌC KỲ FALL 2026")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    # Info summary
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.3
    r = p.add_run("1. Tên đề tài: ")
    r.font.bold = True
    p.add_run("Aquatic Guardian (Hệ Thống Nhúng Thông Minh Giám Sát Nước & Cho Ăn Tự Động)\n")
    r = p.add_run("2. Nhóm sinh viên thực hiện: ")
    r.font.bold = True
    p.add_run("Nhóm 7 — Lớp IC2005 (5 sinh viên: Nghiêm Hoàng Tùng, Hoàng Đức Mạnh, Đỗ Khắc Lê Gia, Phạm Hồng Minh, Nguyễn Đức Anh)\n")
    r = p.add_run("3. Nền tảng kỹ thuật: ")
    r.font.bold = True
    p.add_run("STM32F401RE Nucleo-64 (ARM Cortex-M4), FreeRTOS (CMSIS-RTOS v2), Module Wi-Fi ESP32 IoT Bridge.")

    # 5 Specific Engineering Tasks
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("4. Các nhiệm vụ kỹ thuật cụ thể đã giao và hoàn thành:")
    r.font.bold = True

    tasks = [
        ("Nhiệm vụ 1", "Thiết kế mạch phần cứng không xung đột chân, xử lý sụt áp MB102, cách ly pin RTC và đệm transistor còi."),
        ("Nhiệm vụ 2", "Xây dựng hệ thống đa nhiệm tiền định FreeRTOS gồm 5 tác vụ độc lập, phân bổ stack an toàn chuẩn CMSIS-RTOS v2."),
        ("Nhiệm vụ 3", "Nghiên cứu và hiện thực hóa thuật toán lọc số trung vị/trung bình trượt O(1) và mô hình đa thức bậc 3 bù nhiệt độ TDS."),
        ("Nhiệm vụ 4", "Thiết kế giao thức định khung UART '~' hai chiều, tích hợp module ESP32 kết nối Telegram Bot và Web Dashboard."),
        ("Nhiệm vụ 5", "Kiểm thử thực nghiệm độc lập 4 module, đo lường độ trễ thời gian thực và xây dựng kênh giám sát dự phòng ST-LINK VCP.")
    ]
    for t_id, t_desc in tasks:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.left_indent = Cm(0.8)
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(1)
        r = p_t.add_run(f"• {t_id}: ")
        r.font.bold = True
        p_t.add_run(t_desc)

    # 10.0-Point Rubric Table
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("5. Bảng Tiêu Chí Đánh Giá Đồ Án (Project Assessment Rubric — Thang Điểm 10.0):")
    r.font.bold = True

    rubric_data = [
        ("No.", "Assessment criteria", "Description", "Points"),
        ("1", "Final report", "Assessment of the submitted final report", "1.0"),
        ("2", "Project evaluation", "", ""),
        ("", "Project complexity", "Projects using ESP, HM-10, or similar additional hardware/comm modules", "3.0"),
        ("", "Presentation", "Evaluation of the oral presentation", "1.0"),
        ("", "Block diagram", "Analysis of the operational principle of the system depicted in the diagram", "0.5"),
        ("", "Circuit analysis & assembly", "Evaluation of students' comprehension of their project's execution", "0.5"),
        ("", "Flowchart", "Evaluation of the system programming depicted in the flowchart", "0.5"),
        ("", "Source code analysis", "Evaluation of students' comprehension of their project's execution", "0.5"),
        ("", "Demonstration", "Assessment of how well the system operates according to intended design", "1.0"),
        ("3", "Q&A", "Evaluation of students' comprehension of their project's execution (Oral defense)", "3.0"),
        ("", "TỔNG CỘNG", "Thang điểm tối đa đối với đồ án có module truyền thông ngoài (ESP32)", "10.0 / 10.0")
    ]

    tbl = doc.add_table(rows=len(rubric_data), cols=4)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="707070", sz="4", val="single")

    col_widths = [Cm(1.2), Cm(4.5), Cm(8.0), Cm(2.0)]
    for r_idx, row in enumerate(rubric_data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.width = col_widths[c_idx]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p_c = cell.paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            r = p_c.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            if r_idx == 0 or r_idx == len(rubric_data) - 1 or c_idx == 0 or "complexity" in val:
                r.font.bold = True
            if r_idx == 0:
                set_cell_background(cell, "EAEAEA")
            elif r_idx == len(rubric_data) - 1:
                set_cell_background(cell, "F0F0F0")

    # Signature lines
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(0)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run("Ngày      tháng 11 năm 2026\nGIẢNG VIÊN HƯỚNG DẪN / CHẤM THI\n\n\n\n(Ký và ghi rõ họ tên)                      ")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.italic = True

def add_declaration_and_acknowledgments_page(doc):
    """Builds the Student Declaration and Acknowledgments pages."""
    doc.add_page_break()

    # Lời Cam Đoan
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("LỜI CAM ĐOAN")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(
        "Chúng tôi xin cam đoan đề tài đồ án tốt nghiệp học phần: \"AQUATIC GUARDIAN — HỆ THỐNG NHÚNG THÔNG MINH "
        "GIÁM SÁT CHẤT LƯỢNG NƯỚC VÀ CHO ĂN TỰ ĐỘNG THỜI GIAN THỰC\" là công trình nghiên cứu và thực hiện độc lập của Nhóm 7 (Lớp IC2005) "
        "dưới sự hướng dẫn chuyên môn của các thầy cô trong Hội đồng Bộ môn Lập trình Vi điều khiển (MCP201), Trường Đại học FPT.\n\n"
        "Toàn bộ các số liệu đo đạc thực nghiệm, sơ đồ khối kiến trúc, mạch điện phân tích và toàn văn mã nguồn C FreeRTOS / ESP32 "
        "được trình bày trong báo cáo này là trung thực, minh bạch và không sao chép từ bất kỳ công trình nào chưa được trích dẫn. "
        "Các nguồn tài liệu tham khảo khoa học, thư viện mã nguồn mở và nền tảng kế thừa đều được ghi chú rõ ràng theo đúng tiêu chuẩn trích dẫn học thuật IEEE.\n\n"
        "Nếu có bất kỳ sự gian lận hay vi phạm liêm chính học thuật nào, nhóm chúng tôi xin chịu hoàn toàn trách nhiệm trước Hội đồng chấm thi và Nhà trường."
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)

    # Signature Block for 5 Members
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run("Ngày 14 tháng 11 năm 2026\nĐẠI DIỆN NHÓM SINH VIÊN THỰC HIỆN\n\n\n\nNghiêm Hoàng Tùng (Trưởng nhóm)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    # Lời Cảm Ơn
    doc.add_page_break()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("LỜI CẢM ƠN")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(
        "Lời đầu tiên, Nhóm 7 xin trân trọng gửi lời cảm ơn sâu sắc nhất tới Ban Giám hiệu Trường Đại học FPT, Ban Chủ nhiệm Khoa Vi mạch Bán dẫn & Ô tô số, "
        "cùng toàn thể quý thầy cô giảng viên Bộ môn Lập trình Vi điều khiển (MCP201) đã trang bị cho chúng tôi những nền tảng kiến thức chuyên môn vững chắc, "
        "từ kiến trúc vi xử lý ARM Cortex-M4, nguyên lý hệ điều hành thời gian thực FreeRTOS, kỹ thuật thiết kế phần cứng cho tới tư duy giải quyết vấn đề kỹ thuật thực tế.\n\n"
        "Đặc biệt, nhóm xin chân thành cảm ơn thầy/cô giảng viên trực tiếp hướng dẫn học phần MCP201 đã luôn dành thời gian giải đáp các vướng mắc, "
        "định hướng phương pháp tiếp cận đúng đắn trong quá trình thiết kế sơ đồ không xung đột chân, xử lý sụt áp nguồn và tối ưu hóa các luồng dữ liệu liên tác vụ.\n\n"
        "Dù nhóm đã nỗ lực hết mình để hoàn thiện hệ thống và cuốn báo cáo một cách khoa học, chỉn chu nhất, song do giới hạn về thời gian và kinh nghiệm thực tiễn, "
        "đồ án khó tránh khỏi những điểm thiếu sót nhất định. Nhóm rất mong nhận được những nhận xét, góp ý quý báu từ quý thầy cô trong Hội đồng chấm thi để đề tài được hoàn thiện tốt hơn.\n\n"
        "Nhóm xin kính chúc quý thầy cô luôn dồi dào sức khỏe, hạnh phúc và gặt hái được nhiều thành công trong sự nghiệp giáo dục đào tạo!"
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)

def add_abstract_page(doc):
    """Builds the Bilingual Abstract page (Vietnamese & English)."""
    doc.add_page_break()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("TÓM TẮT ĐỒ ÁN")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.4
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(
        "Đồ án \"Aquatic Guardian\" nghiên cứu và chế tạo thành công một hệ thống nhúng thông minh, hoạt động tự động thời gian thực "
        "nhằm giải quyết triệt để hai nguyên nhân chính gây tử vong ở sinh vật thủy sinh: sai lệch chu kỳ dinh dưỡng và ô nhiễm nguồn nước ngầm. "
        "Hệ thống ứng dụng kiến trúc phân tán hai vi điều khiển (Distributed Dual-MCU): vi điều khiển STM32F401RE (ARM Cortex-M4 @ 84 MHz) "
        "vận hành hệ điều hành FreeRTOS (CMSIS-RTOS v2) đảm nhận 5 tác vụ tiền định thời gian thực; và vi điều khiển ESP32 đóng vai trò Co-Processor "
        "xử lý truyền thông Wi-Fi, tích hợp giao diện điều khiển qua Telegram Bot và Web Dashboard nội bộ.\n\n"
        "Về mặt thuật toán, hệ thống áp dụng bộ lọc trung bình trượt vòng 20 mẫu thực thi trong thời gian O(1) kết hợp phương trình bậc 3 bù nhiệt độ "
        "giúp giảm 96.7% phương sai dao động cảm biến TDS (độ lệch chuẩn giảm từ ±45 ppm xuống dưới ±1.5 ppm). Về mặt đồng bộ hóa, cơ chế hòm thư Length-1 Mailbox "
        "và cơ chế thừa kế quyền ưu tiên (Priority Inheritance) trên bus I2C1 triệt tiêu hoàn toàn hiện tượng chết đói dữ liệu và khóa chết hệ thống. "
        "Kết quả thực nghiệm chứng minh độ trễ phát hiện sự cố đạt 185 ms (thỏa mãn ràng buộc <300 ms), độ trễ ngắt nút bấm đạt 0.85 µs, trong khi chiếm dụng bộ nhớ "
        "chỉ 9.41% Flash ROM và 12.92% SRAM, khẳng định tính ổn định cao và sẵn sàng cho việc mở rộng cảm biến trong tương lai."
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(16)
    r = p.add_run("Từ khóa: ")
    r.font.bold = True
    p.add_run("STM32, FreeRTOS, CMSIS-RTOS v2, ESP32, Telegram Bot, Cảm biến TDS, Xử lý tín hiệu số DSP, Thời gian thực.")

    # English Abstract
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("PROJECT ABSTRACT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.4
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(
        "The \"Aquatic Guardian\" capstone project presents an autonomous, real-time embedded life-support system designed to eliminate "
        "the primary risks of aquatic mortality: irregular feeding cycles and undetected water toxicity or thermal spikes. "
        "The system leverages a distributed dual-microcontroller architecture: an STM32F401RE (ARM Cortex-M4 @ 84 MHz) running FreeRTOS "
        "(CMSIS-RTOS v2) executes 5 deterministic real-time tasks, while an ESP32 co-processor handles Wi-Fi connectivity, Telegram Bot interaction, "
        "and a local responsive Web Dashboard over a robust framed UART protocol.\n\n"
        "Algorithmically, a 20-sample circular moving sum filter running in O(1) time complexity combined with temperature-compensated cubic polynomial "
        "reduces ADC noise variance by 96.7% (standard deviation from ±45 ppm to under ±1.5 ppm). Inter-task communication implements a length-1 mailbox "
        "and Priority Inheritance on the shared I2C1 bus, eliminating data starvation and unbounded priority inversion. Benchmark evaluations verify "
        "hazard detection latency of 185 ms (exceeding the <300 ms deadline) and EXTI button latency of 0.85 µs, with an ultra-lean footprint of "
        "9.41% Flash ROM and 12.92% SRAM, demonstrating deterministic reliability and robust academic rigor."
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run("Keywords: ")
    r.font.bold = True
    p.add_run("STM32, FreeRTOS, CMSIS-RTOS v2, ESP32, Telegram Bot, Water Quality TDS, DSP Filtering, Real-Time Embedded Systems.")

def add_teacher_review_sheet(doc):
    """Builds the Final Review & Grading Sheet for the Examiner Committee."""
    doc.add_page_break()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("NHẬN XÉT VÀ ĐÁNH GIÁ CỦA HỘI ĐỒNG CHẤM THI")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.3
    r = p.add_run("1. Đề tài: ")
    r.font.bold = True
    p.add_run("Aquatic Guardian — Hệ Thống Nhúng Thông Minh Giám Sát Nước & Cho Ăn Tự Động Thời Gian Thực\n")
    r = p.add_run("2. Nhóm sinh viên: ")
    r.font.bold = True
    p.add_run("Nhóm 7 (Lớp IC2005) — 5 thành viên\n")
    r = p.add_run("3. Ý kiến nhận xét của Cán bộ chấm thi:")
    r.font.bold = True

    comments = [
        "a) Về tính cấp thiết, mục tiêu và phạm vi đề tài:",
        "........................................................................................................................................................................................................",
        "b) Về chất lượng quyển báo cáo (bố cục, hình thức, phương trình, trích dẫn học thuật):",
        "........................................................................................................................................................................................................",
        "c) Về kết quả thiết kế mạch điện, sơ đồ khối và giải quyết các bài toán phần cứng thực tế:",
        "........................................................................................................................................................................................................",
        "d) Về chất lượng lập trình vi điều khiển STM32 FreeRTOS và phân hệ IoT ESP32:",
        "........................................................................................................................................................................................................",
        "e) Về kết quả vận hành mô hình thực tế (Demonstration) và trả lời câu hỏi vấn đáp (Q&A):",
        "........................................................................................................................................................................................................"
    ]
    for c_line in comments:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(2)
        p_c.paragraph_format.space_after = Pt(2)
        r = p_c.add_run(c_line)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.5)
        if c_line.startswith(("a)", "b)", "c)", "d)", "e)")):
            r.font.bold = True

    # Final Score Table
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("4. Bảng tổng hợp điểm số đánh giá:")
    r.font.bold = True

    score_tbl_data = [
        ("TT", "Hạng mục đánh giá theo Rubric", "Điểm tối đa", "Điểm CB1", "Điểm CB2", "Điểm Thống nhất"),
        ("1", "File báo cáo kỹ thuật (Final Report)", "1.0", "", "", ""),
        ("2", "Độ phức tạp đề tài (Project Complexity - có ESP32)", "3.0", "", "", ""),
        ("3", "Thuyết trình & bố cục slide (Presentation)", "1.0", "", "", ""),
        ("4", "Sơ đồ khối hệ thống (Block Diagram)", "0.5", "", "", ""),
        ("5", "Phân tích mạch điện & lắp ráp (Circuit Analysis)", "0.5", "", "", ""),
        ("6", "Lưu đồ thuật toán (Flowchart)", "0.5", "", "", ""),
        ("7", "Phân tích mã nguồn C & Firmware (Source Code)", "0.5", "", "", ""),
        ("8", "Trình diễn mô hình thực tế (Demonstration)", "1.0", "", "", ""),
        ("9", "Vấn đáp cá nhân chuyên sâu (Q&A Defense)", "3.0", "", "", ""),
        ("", "TỔNG ĐIỂM ĐỒ ÁN (THANG ĐIỂM 10.0)", "10.0", "", "", "")
    ]

    tbl_s = doc.add_table(rows=len(score_tbl_data), cols=6)
    tbl_s.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_s, color="707070", sz="4", val="single")

    w_cols = [Cm(1.0), Cm(6.5), Cm(2.2), Cm(2.0), Cm(2.0), Cm(2.5)]
    for r_idx, row in enumerate(score_tbl_data):
        for c_idx, val in enumerate(row):
            cell = tbl_s.cell(r_idx, c_idx)
            cell.width = w_cols[c_idx]
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p_c = cell.paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = p_c.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            if r_idx == 0 or r_idx == len(score_tbl_data) - 1:
                r.font.bold = True
            if r_idx == 0:
                set_cell_background(cell, "EAEAEA")
            elif r_idx == len(score_tbl_data) - 1:
                set_cell_background(cell, "F0F0F0")

    # Dual Signature Box
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    sig_tbl = doc.add_table(rows=1, cols=2)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_l = sig_tbl.cell(0, 0)
    cell_r = sig_tbl.cell(0, 1)
    cell_l.width = Cm(8.0)
    cell_r.width = Cm(8.0)

    p_l = cell_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_l = p_l.add_run("CÁN BỘ CHẤM THI 1\n(Ký và ghi rõ họ tên)\n\n\n\n......................................................")
    r_l.font.name = 'Times New Roman'
    r_l.font.size = Pt(11.5)
    r_l.font.bold = True

    p_r = cell_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_r = p_r.add_run("CÁN BỘ CHẤM THI 2\n(Ký và ghi rõ họ tên)\n\n\n\n......................................................")
    r_r.font.name = 'Times New Roman'
    r_r.font.size = Pt(11.5)
    r_r.font.bold = True

def build_report():
    doc = Document()

    # SECTION 1: Outer & Inner Cover Pages
    add_front_cover_page(doc)

    # SECTION 2: Front Matter (Assignment, Declaration, Thanks, Abstract)
    add_assignment_and_rubric_page(doc)
    add_declaration_and_acknowledgments_page(doc)
    add_abstract_page(doc)

    # Set up Table of Contents & Lists as part of Front Matter
    doc.add_page_break()

    # SECTION 3: Main Body (From Chapter 1 onwards, page numbers restart at 1 decimal)
    # We will read markdown file and split at "# CHƯƠNG 1"
    md_path = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\BAO_CAO_DO_AN_AQUATIC_GUARDIAN.md"
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find where Chapter 1 starts
    ch1_idx = 0
    for idx, line in enumerate(lines):
        if line.strip().startswith('# CHƯƠNG 1'):
            ch1_idx = idx
            break

    front_toc_lines = lines[:ch1_idx]
    main_body_lines = lines[ch1_idx:]

    # Render Front Matter TOC lines in Section 2
    render_markdown_lines(doc, front_toc_lines)

    # Now create Section 3 for Main Body
    sec3 = doc.add_section()
    sec3.footer.is_linked_to_previous = False
    sec3.top_margin = Cm(2.5)
    sec3.bottom_margin = Cm(3.0)
    sec3.left_margin = Cm(3.0)
    sec3.right_margin = Cm(2.5)
    sectPr3 = sec3._sectPr
    pgNumType3 = parse_xml(f'<w:pgNumType {nsdecls("w")} w:start="1" w:fmt="decimal"/>')
    sectPr3.append(pgNumType3)

    footer3 = sec3.footer
    f_p3 = footer3.paragraphs[0]
    f_p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_run3 = f_p3.add_run()
    f_run3.font.name = 'Times New Roman'
    f_run3.font.size = Pt(11)
    f_run3.font.color.rgb = RGBColor(0, 0, 0)
    add_page_number(f_run3)

    # Render Main Body lines in Section 3
    render_markdown_lines(doc, main_body_lines)

    # SECTION 4: Final Teacher Review Sheet at the very end
    add_teacher_review_sheet(doc)

    # Save Word document
    out_docx = r"E:\AntiGravityRoot\mcp201-aquatic-guardian\BAO_CAO_DO_AN_AQUATIC_GUARDIAN.docx"
    doc.save(out_docx)
    print(f"[SUCCESS] Complete academic report saved to: {out_docx}")

    # Export directly to PDF via Word COM Automation
    export_to_pdf(out_docx)

def render_markdown_lines(doc, lines):
    """Renders a block of markdown lines into a docx document."""
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

        # Handle Blockquotes
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

        # Handle Dedicated Formula Lines ($$ ... $$)
        if stripped.startswith('$$') and stripped.endswith('$$'):
            content = stripped[2:-2].strip()
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

        # Heading 1: Chapters & Front Matter
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
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Heading 2: Level 1 Sections
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

        # Heading 3: Level 2 Subsections
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

        # Table Captions
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
            run.font.color.rgb = RGBColor(0, 0, 0)

        # Figure Captions
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
            run.font.color.rgb = RGBColor(0, 0, 0)

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

    # Flush remaining
    if in_table and table_lines:
        process_markdown_table(doc, table_lines)
    if in_code and code_lines:
        add_code_block(doc, code_lines)
    if in_quote and quote_lines:
        add_callout_box(doc, quote_lines)

def format_inline_markdown(p, text):
    """Parses markdown links, bold, italic, and code spans in black/colorless style."""
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    pos = 0
    for m in link_pattern.finditer(text):
        pre_text = text[pos:m.start()]
        if pre_text:
            format_inline_spans(p, pre_text)
        
        label = m.group(1).strip()
        url = m.group(2).strip()
        
        is_code = label.startswith('`') and label.endswith('`')
        clean_label = label.strip('`*')
        is_bold = '**' in label
        
        add_hyperlink(p, url, clean_label, is_code=is_code, is_bold=is_bold)
        pos = m.end()
        
    if pos < len(text):
        format_inline_spans(p, text[pos:])

def format_inline_spans(p, text):
    """Parses bold, italic, and code spans in strict monochrome/colorless style."""
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
                run.font.color.rgb = RGBColor(0, 0, 0)

def process_markdown_table(doc, lines):
    """Converts markdown table lines into a styled monochrome Word table."""
    rows_data = []
    for l in lines:
        if '---' in l:
            continue
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
    set_table_borders(table, color="707070", sz="4", val="single")

    for col_idx, text in enumerate(rows_data[0]):
        cell = table.cell(0, col_idx)
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text.replace('**', ''))
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)

    for row_idx in range(1, num_rows):
        r_data = rows_data[row_idx]
        for col_idx in range(num_cols):
            cell = table.cell(row_idx, col_idx)
            val = r_data[col_idx] if col_idx < len(r_data) else ""
            set_cell_background(cell, "FFFFFF")
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 2, 3] and len(val) < 20 else WD_ALIGN_PARAGRAPH.LEFT
            format_inline_markdown(p, val)
            for r in p.runs:
                r.font.size = Pt(11)
                r.font.color.rgb = RGBColor(0, 0, 0)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(8)

def export_to_pdf(docx_path):
    """Exports docx to pdf using Microsoft Word COM Automation."""
    pdf_path = os.path.abspath(docx_path.replace('.docx', '.pdf'))
    new_pdf_path = os.path.abspath(docx_path.replace('.docx', '_NEW.pdf'))
    word = None
    try:
        import win32com.client
        word = win32com.client.Dispatch('Word.Application')
        word.Visible = False
        doc = word.Documents.Open(os.path.abspath(docx_path))
        try:
            doc.SaveAs(pdf_path, FileFormat=17) # 17 = wdFormatPDF
            print(f"[SUCCESS] Official PDF report generated at: {pdf_path}")
        except Exception as e_lock:
            print(f"[NOTE] {pdf_path} is currently locked by a PDF viewer: {e_lock}")
            doc.SaveAs(new_pdf_path, FileFormat=17)
            print(f"[SUCCESS] Saved updated PDF to: {new_pdf_path}")
        doc.Close()
    except Exception as e:
        print(f"[WARNING] Word COM PDF export encountered: {e}")
    finally:
        if word:
            try:
                word.Quit()
            except Exception:
                pass

if __name__ == '__main__':
    build_report()
