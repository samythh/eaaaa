from pathlib import Path
import re

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "05_Laporan_Kemajuan" / "01_Draft" / "Laporan_Kemajuan_EA_Kelompok_4_REVISI.docx"


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def remove_table_borders(table):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = borders.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            borders.append(node)
        node.set(qn("w:val"), "nil")


def set_cell_text(cell, text, bold=False, placeholder=False, size=10, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.alignment = align
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    r.bold = bold
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)
    if placeholder:
        r.italic = True
        r.font.color.rgb = RGBColor(192, 0, 0)
        highlight = OxmlElement("w:highlight")
        highlight.set(qn("w:val"), "yellow")
        r._r.get_or_add_rPr().append(highlight)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def add_caption(doc, text, kind="table"):
    style = "Table Caption" if kind == "table" else "Figure Caption"
    p = doc.add_paragraph(style=style)
    r = p.add_run(text)
    if "[" in text and "]" in text:
        r.italic = True
        r.font.color.rgb = RGBColor(192, 0, 0)
        highlight = OxmlElement("w:highlight")
        highlight.set(qn("w:val"), "yellow")
        r._r.get_or_add_rPr().append(highlight)
    return p


def add_table(doc, headers, rows, widths=None, font_size=10, caption=None):
    if caption:
        add_caption(doc, caption, "table")
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    hdr = table.rows[0]
    set_repeat_table_header(hdr)
    for i, h in enumerate(headers):
        set_cell_text(hdr.cells[i], h, bold=True, size=font_size, align=WD_ALIGN_PARAGRAPH.CENTER)
        if widths:
            hdr.cells[i].width = Cm(widths[i])
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            is_placeholder = "[" in str(value) and "]" in str(value)
            set_cell_text(cells[i], str(value), placeholder=is_placeholder, size=font_size)
            if widths:
                cells[i].width = Cm(widths[i])
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


def add_field(paragraph, instruction, placeholder=""):
    run = paragraph.add_run()
    fld_char = OxmlElement("w:fldChar")
    fld_char.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = instruction
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    result = OxmlElement("w:t")
    result.text = placeholder
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.extend([fld_char, instr_text, fld_sep, result, fld_end])


def add_hyperlink(paragraph, text, url):
    part = paragraph.part
    rel_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), rel_id)
    run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    r_pr.extend([color, underline])
    run.append(r_pr)
    text_element = OxmlElement("w:t")
    text_element.text = text
    run.append(text_element)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def add_body(doc, text="", bold_prefix=None, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(0)
    if bold_prefix and text.startswith(bold_prefix):
        r1 = p.add_run(bold_prefix)
        r1.bold = True
        p.add_run(text[len(bold_prefix):])
    else:
        r = p.add_run(text)
        r.italic = italic
    return p


def add_bullet(doc, text, level=0):
    style = "List Bullet" if level == 0 else "List Bullet 2"
    p = doc.add_paragraph(style=style)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(0)
    p.add_run(text)
    return p


def add_number(doc, text):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(0)
    p.add_run(text)
    return p


def add_placeholder(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("[PERLU DILENGKAPI/DIKONFIRMASI: " + text + "]")
    r.italic = True
    r.font.color.rgb = RGBColor(192, 0, 0)
    highlight = OxmlElement("w:highlight")
    highlight.set(qn("w:val"), "yellow")
    r._r.get_or_add_rPr().append(highlight)
    return p


def add_draft_note(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run("[Draf tim—perlu divalidasi: " + text + "]")
    r.italic = True
    r.font.color.rgb = RGBColor(31, 78, 121)
    return p


def add_source_note(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Sumber: " + text)
    r.italic = True
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_figure_placeholder(doc, caption, prompt):
    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run("[TEMPAT GAMBAR/ARTEFAK]\n" + prompt)
    r.bold = True
    r.font.color.rgb = RGBColor(192, 0, 0)
    highlight = OxmlElement("w:highlight")
    highlight.set(qn("w:val"), "yellow")
    r._r.get_or_add_rPr().append(highlight)
    add_caption(doc, caption, "figure")


def set_update_fields(doc):
    settings = doc.settings._element
    update_fields = settings.find(qn("w:updateFields"))
    if update_fields is None:
        update_fields = OxmlElement("w:updateFields")
        settings.append(update_fields)
    update_fields.set(qn("w:val"), "true")


def configure_document(doc):
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(0)

    for name, size, bold, before, after in [
        ("Title", 14, True, 0, 0),
        ("Heading 1", 12, True, 12, 18),
        ("Heading 2", 12, True, 12, 0),
        ("Heading 3", 12, True, 6, 0),
    ]:
        style = doc.styles[name]
        style.font.name = "Times New Roman"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        style.font.size = Pt(size)
        style.font.bold = bold
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True
    doc.styles["Heading 1"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for chapter in range(1, 5):
        for style_name, base_name, outline_level, alignment, before, after in [
            (f"BAB {chapter}", "Heading 1", 0, WD_ALIGN_PARAGRAPH.CENTER, 12, 18),
            (f"Subbab {chapter}", "Heading 2", 1, WD_ALIGN_PARAGRAPH.LEFT, 12, 0),
            (f"Sub-subbab {chapter}", "Heading 3", 2, WD_ALIGN_PARAGRAPH.LEFT, 6, 0),
        ]:
            if style_name not in [s.name for s in doc.styles]:
                style = doc.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
            else:
                style = doc.styles[style_name]
            style.base_style = doc.styles[base_name]
            style.next_paragraph_style = doc.styles["Normal"]
            style.font.name = "Times New Roman"
            style._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
            style._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
            style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
            style._element.rPr.rFonts.set(qn("w:cs"), "Times New Roman")
            style.font.size = Pt(12)
            style.font.bold = True
            style.font.color.rgb = RGBColor(0, 0, 0)
            style.paragraph_format.alignment = alignment
            style.paragraph_format.space_before = Pt(before)
            style.paragraph_format.space_after = Pt(after)
            style.paragraph_format.keep_with_next = True
            p_pr = style._element.get_or_add_pPr()
            outline = p_pr.find(qn("w:outlineLvl"))
            if outline is None:
                outline = OxmlElement("w:outlineLvl")
                p_pr.append(outline)
            outline.set(qn("w:val"), str(outline_level))
            if style._element.find(qn("w:qFormat")) is None:
                style._element.append(OxmlElement("w:qFormat"))

    for style_name in ["Table Caption", "Figure Caption"]:
        if style_name not in [s.name for s in doc.styles]:
            caption = doc.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
            caption.font.name = "Times New Roman"
            caption._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
            caption.font.size = Pt(12)
            caption.font.italic = True
            caption.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            caption.paragraph_format.space_before = Pt(6)
            caption.paragraph_format.space_after = Pt(6)

    for sec in doc.sections:
        footer = sec.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_field(p, "PAGE", "1")


def apply_chapter_styles(doc):
    """Assign named Word styles per chapter while preserving TOC outline levels."""
    roman_to_number = {"I": 1, "II": 2, "III": 3, "IV": 4}
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        bab_match = re.match(r"^BAB\s+(I|II|III|IV)\b", text)
        if bab_match:
            paragraph.style = doc.styles[f"BAB {roman_to_number[bab_match.group(1)]}"]
            continue
        sub_match = re.match(r"^([1-4])\.(\d+)(?:\.(\d+))?\s", text)
        if sub_match:
            chapter = int(sub_match.group(1))
            style_name = f"Sub-subbab {chapter}" if sub_match.group(3) else f"Subbab {chapter}"
            paragraph.style = doc.styles[style_name]


def force_times_new_roman(doc):
    """Apply Times New Roman to styles and every run, including fields and hyperlinks."""
    for style in doc.styles:
        if style.type not in (WD_STYLE_TYPE.PARAGRAPH, WD_STYLE_TYPE.CHARACTER):
            continue
        style.font.name = "Times New Roman"
        r_pr = style._element.get_or_add_rPr()
        r_fonts = r_pr.find(qn("w:rFonts"))
        if r_fonts is None:
            r_fonts = OxmlElement("w:rFonts")
            r_pr.insert(0, r_fonts)
        for attr in ("ascii", "hAnsi", "eastAsia", "cs"):
            r_fonts.set(qn(f"w:{attr}"), "Times New Roman")

    roots = [doc._element]
    for section in doc.sections:
        roots.extend([section.header._element, section.footer._element])
    seen = set()
    for root in roots:
        if id(root) in seen:
            continue
        seen.add(id(root))
        for run in root.iter(qn("w:r")):
            r_pr = run.get_or_add_rPr()
            r_fonts = r_pr.find(qn("w:rFonts"))
            if r_fonts is None:
                r_fonts = OxmlElement("w:rFonts")
                r_pr.insert(0, r_fonts)
            for attr in ("ascii", "hAnsi", "eastAsia", "cs"):
                r_fonts.set(qn(f"w:{attr}"), "Times New Roman")


def add_cover(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("LAPORAN KEMAJUAN TUGAS BESAR")
    r.bold = True
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    r = p.add_run(
        "ENTERPRISE ARCHITECTURE PENGELOLAAN PERBEKALAN FARMASI PADA "
        "INSTALASI FARMASI RUMAH SAKIT UNIVERSITAS ANDALAS "
        "MENGGUNAKAN TOGAF 9.2"
    )
    r.bold = True
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    r = p.add_run("Disusun untuk Memenuhi Tugas Mata Kuliah\nEnterprise Architecture")
    r.italic = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.add_run("Dosen Pengampu:\nAdi Arga Arifnur, M.Kom")

    logo_path = ROOT / "00_Manajemen_Proyek" / "assets" / "logo_unand.png"
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    if logo_path.exists():
        p.add_run().add_picture(str(logo_path), width=Cm(5.2))
    else:
        p.add_run("[LOGO UNIVERSITAS ANDALAS]").bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.add_run("Disusun Oleh:")
    members = [
        ("Mikail Samyth Habibillah", "2411523016"),
        ("Mutiara Ayudya Ramadhani", "2411523008"),
        ("Firzatunnisa", "2411523011"),
        ("Taris Rafivdean", "2411523013"),
        ("Sheva Ramadhan", "2411523020"),
        ("Ihsan Auliya Habiburrahim", "2411523022"),
    ]
    member_table = doc.add_table(rows=len(members), cols=2)
    member_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    member_table.autofit = False
    remove_table_borders(member_table)
    for idx, (name, nim) in enumerate(members):
        set_cell_text(member_table.cell(idx, 0), name, size=11)
        set_cell_text(member_table.cell(idx, 1), nim, size=11)
        member_table.cell(idx, 0).width = Cm(7)
        member_table.cell(idx, 1).width = Cm(3.5)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Kelompok: 4")

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    r = p.add_run(
        "DEPARTEMEN SISTEM INFORMASI\n"
        "FAKULTAS TEKNOLOGI INFORMASI\n"
        "UNIVERSITAS ANDALAS\n"
        "2026"
    )
    r.bold = True
    doc.add_page_break()


def add_approval(doc):
    doc.add_heading("LEMBAR PERSETUJUAN", level=1)
    add_body(
        doc,
        "Laporan Kemajuan Tugas Besar yang berjudul “Enterprise Architecture Pengelolaan Perbekalan Farmasi pada Instalasi Farmasi Rumah Sakit Universitas Andalas Menggunakan TOGAF 9.2” ini disusun sebagai dokumentasi kemajuan perancangan arsitektur enterprise pada ruang lingkup yang ditetapkan. Laporan memuat persiapan kapabilitas arsitektur, perumusan visi arsitektur, serta pemetaan arsitektur bisnis berdasarkan data yang diperoleh melalui studi dokumen, wawancara, dan observasi terbatas. Setiap usulan dalam laporan merupakan hasil analisis akademik tim dan tidak dinyatakan sebagai keputusan implementasi Rumah Sakit Universitas Andalas."
    )
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.add_run("Padang, ")
    r = p.add_run("[TANGGAL PERSETUJUAN]")
    r.italic = True
    r.font.color.rgb = RGBColor(192, 0, 0)
    highlight = OxmlElement("w:highlight")
    highlight.set(qn("w:val"), "yellow")
    r._r.get_or_add_rPr().append(highlight)
    p.add_run(" 2026")
    sig = doc.add_table(rows=1, cols=2)
    sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig.autofit = False
    remove_table_borders(sig)
    set_cell_text(sig.cell(0, 0), "Ketua Tim Arsitek\n\n\n\nMikail Samyth Habibillah\nNIM. 2411523016", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=11)
    set_cell_text(sig.cell(0, 1), "Pimpinan Organisasi/Bagian\n\n\n\n[Nama Lengkap]\n[Jabatan/NIP]", bold=True, placeholder=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=11)
    sig.cell(0, 0).width = Cm(8)
    sig.cell(0, 1).width = Cm(8)
    doc.add_page_break()


def add_front_matter(doc):
    doc.add_heading("KATA PENGANTAR", level=1)
    add_body(doc, "Laporan kemajuan ini disusun untuk memenuhi tugas besar mata kuliah Enterprise Architecture pada Program Studi Sistem Informasi, Fakultas Teknologi Informasi, Universitas Andalas. Kegiatan diarahkan pada pemetaan pengelolaan perbekalan farmasi di Instalasi Farmasi Rumah Sakit Universitas Andalas menggunakan TOGAF 9.2, dengan cakupan laporan kemajuan pada Preliminary Phase, Architecture Vision, dan Business Architecture.")
    add_body(doc, "Penyusunan laporan dilakukan secara bertahap melalui studi dokumen, wawancara, observasi terbatas, pemodelan, serta analisis kondisi saat ini dan kondisi yang diusulkan. Tim membatasi pengumpulan data pada alur proses dan informasi organisasi yang relevan. Data pasien, resep, informasi keuangan rinci, serta konfigurasi keamanan sistem tidak menjadi bagian dari kegiatan.")
    add_body(doc, "Tim menyampaikan terima kasih kepada apt. Dirgan Yolanda, S.Farm., selaku Kepala Ruangan/Penanggung Jawab Gudang Farmasi RS Unand, yang telah memberikan penjelasan mengenai proses pengelolaan perbekalan farmasi. Tim juga berterima kasih kepada pihak RS Unand yang telah memfasilitasi kegiatan observasi dan wawancara.")
    add_body(doc, "Tim menyadari bahwa dokumen ini merupakan laporan kemajuan. Karena itu, setiap temuan dan usulan yang belum memperoleh konfirmasi dinyatakan secara terbuka sebagai bagian yang masih memerlukan validasi. Kritik dan masukan diharapkan dapat membantu penyempurnaan hasil pada tahap berikutnya.")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.add_run("Padang, ")
    r = p.add_run("[TANGGAL FINALISASI]")
    r.italic = True
    r.font.color.rgb = RGBColor(192, 0, 0)
    highlight = OxmlElement("w:highlight")
    highlight.set(qn("w:val"), "yellow")
    r._r.get_or_add_rPr().append(highlight)
    p.add_run("\n\nTim Arsitek")
    doc.add_page_break()

    doc.add_heading("DAFTAR ISI", level=1)
    p = doc.add_paragraph()
    add_field(p, 'TOC \\o "1-3" \\h \\z \\u', "Klik kanan → Update Field setelah dokumen dibuka di Microsoft Word.")
    doc.add_page_break()

    doc.add_heading("DAFTAR GAMBAR", level=1)
    p = doc.add_paragraph()
    add_field(p, 'TOC \\h \\z \\t "Figure Caption,1"', "Perbarui setelah semua gambar dimasukkan.")
    doc.add_page_break()

    doc.add_heading("DAFTAR TABEL", level=1)
    p = doc.add_paragraph()
    add_field(p, 'TOC \\h \\z \\t "Table Caption,1"', "Perbarui setelah semua tabel difinalkan.")
    doc.add_page_break()

    doc.add_heading("DAFTAR LAMPIRAN", level=1)
    for item in [
        "Lampiran A — Instrumen dan daftar pertanyaan wawancara",
        "Lampiran B — Dokumentasi observasi/wawancara",
        "Lampiran C — Ringkasan atau transkrip wawancara",
        "Lampiran D — Dokumen pendukung yang diizinkan RS",
        "Lampiran E — Matriks ketertelusuran sumber dan temuan",
    ]:
        add_bullet(doc, item)
    doc.add_page_break()


def add_chapter_1(doc):
    doc.add_heading("BAB I PENDAHULUAN", level=1)
    doc.add_heading("1.1 Latar Belakang", level=2)
    add_body(doc, "Organisasi layanan kesehatan menjalankan proses yang melibatkan banyak fungsi, profesi, informasi, dan teknologi. Perubahan pada satu bagian dapat memengaruhi bagian lain sehingga perbaikan tidak cukup dilakukan dengan melihat aplikasi atau aktivitas secara terpisah. Enterprise Architecture (EA) menyediakan cara untuk menggambarkan proses bisnis dan sistem informasi beserta hubungannya, kemudian mengarahkan perubahan menuju kondisi yang mendukung tujuan organisasi. Tamm et al. (2011) menjelaskan bahwa nilai EA muncul melalui penyelarasan organisasi, ketersediaan informasi, optimalisasi portofolio sumber daya, dan komplementaritas sumber daya. Penelitian yang lebih baru juga menunjukkan bahwa EA dapat membantu memperbaiki pengambilan keputusan sistem informasi, pelaksanaan proyek, dan kesesuaian platform informasi dengan kebutuhan organisasi (Tamm et al., 2022).")
    add_body(doc, "Manfaat tersebut tidak terjadi secara otomatis hanya karena organisasi menghasilkan diagram arsitektur. Gong dan Janssen (2019) mengingatkan bahwa klaim manfaat EA harus dinilai sesuai konteks dan didukung bukti. Shanks et al. (2018) juga menunjukkan bahwa nilai EA berkaitan dengan kemampuan organisasi menggunakan pengetahuan, standar, partisipasi pemangku kepentingan, dan layanan arsitektur untuk mendukung perubahan. Atas dasar itu, pemetaan dalam tugas ini disusun dari data lapangan, dokumen yang dapat ditelusuri, dan hubungan yang jelas antara kondisi saat ini, tujuan, usulan kondisi target, serta kesenjangannya.")
    add_body(doc, "Rumah Sakit Universitas Andalas (RS Unand) merupakan Rumah Sakit Perguruan Tinggi Negeri yang dikelola Universitas Andalas. Laman resmi RS Unand menyatakan bahwa rumah sakit mulai beroperasi pada 29 Maret 2017 dan saat ini memberikan layanan kesehatan sekaligus menjalankan fungsi pendidikan dan penelitian. Instalasi farmasi tercantum sebagai salah satu layanan rumah sakit. Visi resmi RS Unand adalah menjadi rumah sakit pendidikan terkemuka dan bermartabat di Indonesia, dengan misi yang mencakup pelayanan berbasis bukti, pendidikan, penelitian, tata kelola yang unggul, serta kerja sama berkelanjutan (RS Universitas Andalas, n.d.-a, n.d.-b).")
    add_body(doc, "Pengelolaan perbekalan farmasi dipilih karena mencakup rangkaian kegiatan yang saling bergantung, mulai dari pemilihan, perencanaan, pengadaan, penerimaan, penyimpanan, distribusi, pengendalian, penanganan barang kedaluwarsa atau rusak, hingga pelaporan. Berdasarkan wawancara dengan apt. Dirgan Yolanda, S.Farm., Kepala Ruangan/Penanggung Jawab Gudang Farmasi RS Unand, pada 29 September 2026, sebagian besar tahapan tersebut telah didukung SIMRS Transmedic. Namun, perhitungan kebutuhan masih diolah menggunakan Excel dari data konsumsi SIMRS; klasifikasi fast moving, slow moving, dead stock, serta VEN juga masih dilakukan secara manual.")
    add_body(doc, "Wawancara juga mengidentifikasi dua kendala yang perlu dikaji lebih lanjut, yaitu ketidaksesuaian nilai harga pada keluaran laporan dengan data yang dimasukkan dan kemungkinan transaksi tercatat ganda setelah proses pertama mengalami error lalu diulang. Narasumber menekankan kebutuhan ketertelusuran untuk membantu investigasi selisih atau kehilangan stok, serta mengharapkan fungsi peringatan stok minimum dan pencatatan batch serta kedaluwarsa yang lebih baik. Temuan tersebut diperlakukan sebagai keterangan narasumber yang masih perlu dikonfirmasi dengan bagian sistem informasi dan bukti teknis, bukan sebagai kesimpulan bahwa seluruh SIMRS bermasalah.")
    add_body(doc, "Kerangka yang digunakan adalah TOGAF 9.2. TOGAF menyediakan Architecture Development Method (ADM) sebagai metode iteratif untuk mengembangkan arsitektur. Pembahasan laporan kemajuan ini dibatasi pada Preliminary Phase, Phase A: Architecture Vision, dan Phase B: Business Architecture (The Open Group, 2018). Preliminary Phase menyiapkan ruang lingkup, tata kelola, prinsip, tim, serta alat kerja. Architecture Vision menetapkan arah dan batas inisiatif, sedangkan Business Architecture menggambarkan organisasi, fungsi, peran, serta proses bisnis baseline dan target sebagai dasar analisis kesenjangan.")

    doc.add_heading("1.2 Rumusan Masalah", level=2)
    add_body(doc, "Berdasarkan ruang lingkup kegiatan dan hasil wawancara awal, rumusan masalah laporan kemajuan adalah sebagai berikut:")
    for text in [
        "Bagaimana ruang lingkup, pemangku kepentingan, prinsip, tata kelola, tim, metode, dan alat yang diperlukan untuk pelaksanaan Enterprise Architecture pada pengelolaan perbekalan farmasi di Instalasi Farmasi RS Unand?",
        "Bagaimana kondisi Business Architecture pengelolaan perbekalan farmasi saat ini, meliputi peran, tahapan proses, sistem pendukung, risiko, indikator, dan acuan kerja?",
        "Bagaimana proses manual, kebutuhan ketertelusuran stok, serta kendala pencatatan transaksi yang disampaikan narasumber dapat dirumuskan sebagai kebutuhan arsitektur tanpa melampaui bukti yang tersedia?",
        "Kondisi target apa yang layak diusulkan berdasarkan temuan, Architecture Goals, dan Architecture Principles; serta kesenjangan apa yang perlu ditangani?",
    ]:
        add_number(doc, text)
    add_source_note(doc, "Wawancara dengan apt. Dirgan Yolanda, S.Farm., 29 September 2026; temuan teknis masih memerlukan klarifikasi kepada bagian IT.")

    doc.add_heading("1.3 Ruang Lingkup", level=2)
    add_body(doc, "Ruang lingkup kegiatan ditetapkan agar pengumpulan data dan analisis tetap terarah. Batasan yang digunakan adalah sebagai berikut:")
    for text in [
        "Objek organisasi adalah Instalasi Farmasi RS Unand dengan titik observasi pada Gudang Farmasi.",
        "Objek proses adalah pengelolaan perbekalan farmasi yang mencakup pemilihan, perencanaan kebutuhan, pengadaan/pemesanan, penerimaan, penyimpanan, distribusi, pengendalian persediaan, penanganan barang kedaluwarsa/rusak, dan pelaporan.",
        "Cakupan metode laporan kemajuan adalah Preliminary Phase, Phase A: Architecture Vision, dan Phase B: Business Architecture TOGAF 9.2.",
        "Pembahasan sistem informasi dan teknologi hanya dicatat sebagai konteks awal atau kebutuhan lanjutan; analisis rinci Phase C dan Phase D tidak dinyatakan selesai dalam laporan kemajuan ini.",
        "Kegiatan tidak mengumpulkan data pasien, rekam medis, resep, harga atau data keuangan rinci, konfigurasi jaringan, alamat server, mekanisme keamanan, maupun informasi sensitif lain yang tidak diperlukan.",
        "Usulan TO-BE merupakan hasil analisis akademik tim dan bukan keputusan atau komitmen implementasi RS Unand.",
    ]:
        add_bullet(doc, text)

    doc.add_heading("1.4 Tujuan dan Manfaat", level=2)
    doc.add_heading("1.4.1 Tujuan", level=3)
    for text in [
        "Menetapkan dasar pelaksanaan arsitektur yang mencakup ruang lingkup, pemangku kepentingan, tim, prinsip, metode, dan alat.",
        "Merumuskan Architecture Vision yang menghubungkan arah organisasi dengan fokus pengelolaan perbekalan farmasi.",
        "Mendokumentasikan Business Architecture baseline secara objektif berdasarkan bukti lapangan.",
        "Menyusun rancangan target, analisis kesenjangan, dan rekomendasi yang dapat ditelusuri ke masalah serta tujuan arsitektur.",
    ]:
        add_bullet(doc, text)
    doc.add_heading("1.4.2 Manfaat", level=3)
    add_body(doc, "Bagi tim mahasiswa, kegiatan ini menjadi penerapan TOGAF 9.2 pada kasus organisasi nyata dan latihan menjaga konsistensi antara bukti, model, serta rekomendasi. Bagi pihak RS Unand, hasilnya diharapkan dapat menjadi dokumentasi akademik mengenai alur kerja dan bahan masukan awal. Dokumen ini tidak dimaksudkan sebagai rancangan implementasi siap pakai; setiap usulan tetap memerlukan evaluasi serta keputusan pihak RS.")


def add_chapter_2(doc):
    doc.add_page_break()
    doc.add_heading("BAB II LANDASAN TEORI", level=1)
    doc.add_heading("2.1 Enterprise Architecture", level=2)
    add_body(doc, "Enterprise Architecture merupakan representasi tingkat tinggi mengenai proses bisnis, sistem informasi, hubungan antarkomponen, dan arah pengembangannya. EA tidak terbatas pada teknologi. Ia menghubungkan proses, struktur, informasi, aplikasi, teknologi, dan tanggung jawab pengelolaan agar keputusan perubahan dapat dinilai dalam konteks organisasi secara utuh (Tamm et al., 2011; Hazen et al., 2017). ISO/IEC/IEEE 42010:2022 membedakan arsitektur dari architecture description, yaitu artefak kerja yang dipakai untuk mengekspresikan arsitektur bagi tujuan dan pemangku kepentingan tertentu (ISO/IEC/IEEE, 2022).")
    add_body(doc, "Kajian empiris menunjukkan bahwa EA dapat membantu organisasi melalui penyediaan informasi yang lebih terstruktur, koordinasi proyek, standar, dan penyelarasan platform informasi dengan kebutuhan bisnis. Namun, manfaat itu bergantung pada penggunaan artefak, partisipasi pemangku kepentingan, tata kelola, dan konteks organisasi; EA bukan solusi otomatis untuk seluruh persoalan (Shanks et al., 2018; Gong & Janssen, 2019; Tamm et al., 2022). Prinsip ini digunakan dalam laporan dengan membatasi klaim hanya pada temuan yang didukung bukti.")

    doc.add_heading("2.2 TOGAF 9.2", level=2)
    add_body(doc, "TOGAF 9.2 adalah standar dan kerangka Enterprise Architecture yang diterbitkan The Open Group. Bagian inti TOGAF adalah Architecture Development Method (ADM), yaitu metode iteratif yang terdiri atas Preliminary Phase, Phase A sampai Phase H, serta Requirements Management yang berjalan sepanjang siklus. ADM dapat disesuaikan dengan kebutuhan, ruang lingkup, dan tingkat kedalaman organisasi (The Open Group, 2018).")
    add_figure_placeholder(doc, "Gambar 2.1 Siklus TOGAF ADM 9.2", "Masukkan gambar yang dibuat ulang oleh tim atau diagram dari sumber resmi sesuai ketentuan lisensi; cantumkan sumber The Open Group (2018).")
    add_source_note(doc, "The Open Group (2018), The TOGAF Standard, Version 9.2, Part II.")

    doc.add_heading("2.3 Preliminary Phase", level=2)
    add_body(doc, "Preliminary Phase mempersiapkan organisasi untuk menjalankan pekerjaan arsitektur. Kegiatannya mencakup penentuan organisasi yang terdampak, tata kelola, tim dan tanggung jawab, prinsip arsitektur, penyesuaian metode, serta strategi alat dan teknik. Dengan demikian, fase ini menjawab lokasi penerapan, hal yang diatur, alasan, pelaksana, dan cara kerja arsitektur (The Open Group, 2018).")

    doc.add_heading("2.4 Architecture Vision", level=2)
    add_body(doc, "Phase A: Architecture Vision menetapkan inisiatif arsitektur pada tingkat tinggi. Fase ini mengidentifikasi pemangku kepentingan dan perhatian mereka, mengonfirmasi tujuan serta ruang lingkup, dan merumuskan gambaran kondisi target serta nilai yang ingin dicapai. Architecture Vision menjadi rujukan bagi pengembangan arsitektur yang lebih rinci pada fase berikutnya (The Open Group, 2018).")

    doc.add_heading("2.5 Business Architecture", level=2)
    add_body(doc, "Phase B: Business Architecture mengembangkan gambaran cara organisasi beroperasi untuk mencapai tujuan dan merespons pendorong yang disepakati pada Architecture Vision. Unsur yang relevan mencakup struktur organisasi, peran, fungsi, layanan, proses, aturan, dan informasi bisnis. TOGAF mengarahkan penyusunan baseline, target, gap analysis, serta kandidat komponen roadmap berdasarkan kesenjangan di antara keduanya (The Open Group, 2018).")
    add_body(doc, "TOGAF membedakan keluaran arsitektur menjadi deliverable, artifact, dan building block; artifact dapat berbentuk katalog, matriks, atau diagram (The Open Group, 2018). Berdasarkan struktur tersebut, Business Architecture dalam laporan ini direpresentasikan melalui Business Principles, Organization Role Diagram, Risk Diagram, KPI Diagram, Standard and Regulation, Business Process Diagram, Functional Decomposition Diagram, matriks keterkaitan, Business Interaction Matrix, serta Gap Analysis. Pemilihan artefak disesuaikan dengan ruang lingkup pengelolaan perbekalan dan ketersediaan bukti.")

    doc.add_heading("2.6 Baseline, Target, dan Gap Analysis", level=2)
    add_body(doc, "Baseline menggambarkan kondisi yang sedang berjalan sebagaimana adanya, sedangkan target menggambarkan kondisi yang ingin dicapai. Gap analysis membandingkan keduanya untuk mengidentifikasi unsur yang dipertahankan, diubah, dihapus, atau ditambahkan. Model baseline tidak boleh dibuat lebih ideal daripada keadaan nyata karena hal tersebut menghilangkan dasar analisis kesenjangan. Sebaliknya, target tidak boleh dirancang lepas dari tujuan, prinsip, kebutuhan, dan batasan yang telah ditetapkan (The Open Group, 2018).")

    doc.add_heading("2.7 Business Process Model and Notation", level=2)
    add_body(doc, "Business Process Model and Notation (BPMN) adalah notasi standar untuk menggambarkan proses bisnis sehingga alur aktivitas, peristiwa, keputusan, peserta, dan pertukaran pesan dapat dipahami secara konsisten. Dalam laporan ini, BPMN digunakan untuk merepresentasikan kondisi AS-IS dan TO-BE pada proses yang berada dalam ruang lingkup. Penggunaan simbol mengikuti BPMN Version 2.0.2 dari Object Management Group (OMG, 2014).")

    doc.add_heading("2.8 Enterprise Architecture pada Organisasi Kesehatan", level=2)
    add_body(doc, "Lingkungan kesehatan memiliki kebutuhan koordinasi dan pertukaran informasi yang kompleks. Adenuga et al. (2015) membahas EA sebagai pendekatan untuk melihat integrasi serta interoperabilitas sistem kesehatan dalam konteks proses, data, dan layanan. Relevansi kajian tersebut bagi tugas ini berada pada kebutuhan melihat hubungan antarkomponen, bukan pada anggapan bahwa kondisi RS Unand sama dengan kasus penelitian tersebut. Oleh sebab itu, temuan lapangan tetap menjadi sumber utama dalam menggambarkan konteks Instalasi Farmasi RS Unand.")


def add_chapter_3(doc):
    doc.add_page_break()
    doc.add_heading("BAB III METODE PELAKSANAAN", level=1)
    doc.add_heading("3.1 Pendekatan Kegiatan", level=2)
    add_body(doc, "Kegiatan menggunakan pendekatan studi kasus deskriptif. Fokusnya adalah memperoleh pemahaman kontekstual mengenai pengelolaan perbekalan farmasi pada satu unit organisasi, kemudian menyusun deskripsi arsitektur dan usulan perbaikan dengan TOGAF 9.2. Istilah deskriptif digunakan karena laporan terlebih dahulu menggambarkan kondisi yang ditemukan; laporan tidak menguji efektivitas klinis atau membuat generalisasi untuk seluruh rumah sakit.")

    doc.add_heading("3.2 Subjek dan Objek", level=2)
    add_table(
        doc,
        ["Komponen", "Keterangan"],
        [
            ("Subjek", "apt. Dirgan Yolanda, S.Farm., Kepala Ruangan/Penanggung Jawab Gudang Farmasi RS Unand"),
            ("Objek organisasi", "Instalasi Farmasi Rumah Sakit Universitas Andalas dengan titik observasi pada Gudang Farmasi"),
            ("Objek proses", "Pengelolaan perbekalan farmasi dalam batas yang disetujui narasumber"),
            ("Objek arsitektur", "Preliminary Phase, Architecture Vision, dan Business Architecture"),
        ],
        widths=[4, 12],
        caption="Tabel 3.1 Subjek dan Objek Kegiatan",
    )

    doc.add_heading("3.3 Teknik Pengumpulan Data", level=2)
    add_table(
        doc,
        ["Teknik", "Tujuan", "Bukti", "Status"],
        [
            ("Studi dokumen", "Memperoleh profil, visi–misi, struktur, SOP, indikator, dan acuan kerja", "Laman resmi RS, dokumen resmi yang diizinkan, bahan mata kuliah", "Berjalan; dokumen internal menunggu izin"),
            ("Wawancara semiterstruktur", "Menggali peran, alur, sistem, risiko, indikator, aturan, kendala, dan kebutuhan", "Rekaman dengan izin, catatan anggota, ringkasan jawaban", "Terlaksana 29 September 2026 bersama apt. Dirgan Yolanda, S.Farm.; [LENGKAPI DURASI]"),
            ("Observasi terbatas", "Memahami urutan kegiatan dan konteks fisik tanpa melihat isi data sensitif", "Catatan observasi dan foto yang diizinkan", "Terlaksana pada area yang diizinkan; [LENGKAPI OBJEK YANG DIAMATI]"),
            ("Klarifikasi/member checking", "Memeriksa pemahaman tim atas BPMN AS-IS dan istilah proses", "Pesan, catatan pertemuan, atau paraf/konfirmasi", "[ISI RENCANA/REALISASI]"),
        ],
        widths=[3, 6, 5, 4],
        font_size=9,
        caption="Tabel 3.2 Teknik Pengumpulan Data",
    )

    doc.add_heading("3.4 Keabsahan dan Ketertelusuran Data", level=2)
    add_body(doc, "Keabsahan dijaga melalui perbandingan antar-sumber, yaitu jawaban narasumber, hasil observasi, dan dokumen yang dapat ditelusuri. Setiap temuan penting dicatat bersama sumber atau penanda waktu rekaman. Bila informasi berbeda, laporan tidak memilih salah satu secara sembarangan; perbedaan dicatat dan diklarifikasi. Model AS-IS direncanakan untuk diperiksa kembali oleh narasumber atau pihak yang memahami proses. Analisis tim dipisahkan dari fakta organisasi agar pembaca dapat mengetahui asal setiap pernyataan.")

    doc.add_heading("3.5 Alur Pelaksanaan", level=2)
    steps = [
        ("Persiapan", "Menetapkan objek, mengurus perizinan, menyiapkan instrumen, dan mempelajari acuan."),
        ("Pengumpulan data", "Melakukan studi dokumen, wawancara, observasi, dan pengumpulan dokumentasi yang diizinkan."),
        ("Konsolidasi", "Menggabungkan catatan, mengamankan rekaman, menyusun daftar istilah, dan menandai data yang belum pasti."),
        ("Preliminary Phase", "Menetapkan ruang lingkup, stakeholder, tim, prinsip, tailoring, serta tools."),
        ("Architecture Vision", "Merumuskan tujuan, perhatian stakeholder, nilai, ruang lingkup, dan visi target tingkat tinggi."),
        ("Business Architecture", "Menyusun baseline, memvalidasi AS-IS, merancang target, dan melakukan gap analysis."),
        ("Pelaporan", "Menyatukan narasi, tabel, artefak, referensi, dokumentasi, dan hasil pemeriksaan akhir."),
    ]
    add_table(doc, ["Tahap", "Aktivitas"], steps, widths=[4, 12], caption="Tabel 3.3 Alur Pelaksanaan")
    add_figure_placeholder(doc, "Gambar 3.1 Alur Pelaksanaan Tugas Besar", "Buat diagram dari tujuh tahap pada tabel di atas menggunakan gaya visual yang konsisten.")

    doc.add_heading("3.6 Tailoring TOGAF ADM", level=2)
    add_body(doc, "TOGAF 9.2 bersifat generik sehingga diterapkan sesuai konteks tugas. Pada laporan kemajuan, siklus dibatasi pada persiapan dan pengembangan arsitektur bisnis. Fase E sampai H tidak dikerjakan karena implementasi, perencanaan migrasi, dan governance implementasi berada di luar cakupan tugas yang dirangkum. Phase C dan Phase D disiapkan untuk tahap lanjutan apabila diwajibkan. Requirements Management diperlakukan sebagai kegiatan yang berjalan selama pengumpulan, pemodelan, dan klarifikasi kebutuhan.")
    add_table(
        doc,
        ["Bagian TOGAF", "Penerapan dalam tugas", "Status"],
        [
            ("Preliminary Phase", "Ruang lingkup, stakeholder, tim, prinsip, tailoring, tools", "Dikerjakan"),
            ("Phase A", "Architecture Vision dan tujuan arsitektur", "Dikerjakan"),
            ("Phase B", "Business Architecture baseline, target, dan gap", "Dikerjakan"),
            ("Phase C–D", "Data, aplikasi, dan teknologi", "Disiapkan untuk tahap lanjutan"),
            ("Phase E–H", "Solusi, migrasi, implementasi, perubahan", "Di luar ruang lingkup"),
            ("Requirements Management", "Pencatatan dan validasi kebutuhan sepanjang proses", "Berjalan lintas fase"),
        ],
        widths=[4, 9, 4],
        caption="Tabel 3.4 Tailoring TOGAF ADM",
    )

    doc.add_heading("3.7 Jadwal Pelaksanaan", level=2)
    add_table(
        doc,
        ["No.", "Kegiatan", "Rencana", "Realisasi", "Bukti"],
        [
            ("1", "Pemilihan objek dan penyusunan instrumen", "September 2026", "[ISI]", "Instrumen/proposal"),
            ("2", "Pengurusan surat/perizinan", "September 2026", "Selesai menurut pembaruan ketua tim", "[MASUKKAN NOMOR/TANGGAL SURAT]"),
            ("3", "Wawancara dan observasi", "29 September 2026", "Terlaksana", "Rekaman, catatan, dan [MASUKKAN FOTO TERPILIH]"),
            ("4", "Konsolidasi dan pemodelan", "29–30 September 2026", "[ISI]", "Model/tabel"),
            ("5", "Validasi AS-IS", "[ISI RENCANA]", "[ISI]", "Bukti konfirmasi"),
            ("6", "Finalisasi laporan kemajuan", "[ISI TENGGAT RESMI]", "[ISI]", "Dokumen final"),
        ],
        widths=[1, 5, 3, 4, 4],
        font_size=9,
        caption="Tabel 3.5 Jadwal Pelaksanaan",
    )

    doc.add_heading("3.8 Tim Arsitek", level=2)
    add_table(
        doc,
        ["Nama", "NIM", "Peran", "Tanggung jawab utama"],
        [
            ("Mikail Samyth Habibillah", "2411523016", "Lead Architect", "Koordinasi, komunikasi dengan RS, dan pengendalian konsistensi"),
            ("Mutiara Ayudya Ramadhani", "2411523008", "Business Architect", "Pemetaan alur kerja dan BPMN"),
            ("Firzatunnisa", "2411523011", "Data & Application Architect", "Pencatatan sistem, data, dan sesi IT"),
            ("Taris Rafivdean", "2411523013", "Technology Architect", "Risiko, indikator, regulasi, dan konteks teknologi"),
            ("Sheva Ramadhan", "2411523020", "Documentation & Requirements", "Unit, mitra, sumber daya, peran, dan dokumen"),
            ("Ihsan Auliya Habiburrahim", "2411523022", "Documentation & Requirements", "Dokumentasi foto/video dan bukti kegiatan"),
        ],
        widths=[4.5, 3, 4, 6],
        font_size=9,
        caption="Tabel 3.6 Pembagian Peran Tim Arsitek",
    )
    add_source_note(doc, "Pembagian peran internal tim.")

    doc.add_heading("3.9 Identifikasi Stakeholder", level=2)
    add_body(doc, "Sesuai arahan mata kuliah, stakeholder internal pada tugas ini adalah tim arsitek mahasiswa, sedangkan stakeholder eksternal adalah pihak organisasi yang diteliti. Daftar eksternal berikut belum boleh dianggap final sebelum peran dan kewenangannya dikonfirmasi.")
    add_table(
        doc,
        ["Stakeholder", "Kategori", "Kepentingan/kontribusi", "Status bukti"],
        [
            ("Tim arsitek mahasiswa", "Internal", "Melaksanakan pengumpulan data, pemodelan, analisis, dan pelaporan", "Terkonfirmasi oleh pembagian tim"),
            ("Kepala/penanggung jawab Instalasi Farmasi", "Eksternal", "Kewenangan, kebijakan unit, dan validasi proses", "[KONFIRMASI NAMA/JABATAN]"),
            ("Staf yang menjalankan proses", "Eksternal", "Informasi operasional AS-IS", "[KONFIRMASI PERAN]"),
            ("Bidang/unit terkait", "Eksternal", "Interaksi lintas unit", "[IDENTIFIKASI DARI WAWANCARA]"),
            ("Bagian sistem informasi/IT", "Eksternal", "Konteks aplikasi, data, integrasi, dan teknologi", "[KONFIRMASI SESI/NARASUMBER]"),
        ],
        widths=[4, 2.5, 7, 4.5],
        font_size=9,
        caption="Tabel 3.7 Identifikasi Stakeholder",
    )

    doc.add_heading("3.10 Tools", level=2)
    add_table(
        doc,
        ["Tools", "Penggunaan"],
        [
            ("Sparx Enterprise Architect", "Penyusunan dan penyimpanan artefak arsitektur serta BPMN"),
            ("Microsoft Word", "Penyusunan laporan"),
            ("Spreadsheet", "Konsolidasi data, matriks, dan pemeriksaan konsistensi"),
            ("Perekam audio/kamera", "Dokumentasi setelah memperoleh izin"),
            ("Penyimpanan kelompok", "Cadangan bukti dengan akses terbatas"),
        ],
        widths=[5, 11],
        caption="Tabel 3.8 Tools yang Digunakan",
    )

    doc.add_heading("3.11 Etika dan Perlindungan Informasi", level=2)
    add_body(doc, "Pengumpulan data berfokus pada alur proses, bukan isi data. Rekaman dan foto hanya dibuat setelah memperoleh izin. Tim tidak meminta atau memasukkan data pasien, resep, informasi harga/keuangan rinci, kredensial, alamat server, konfigurasi jaringan, mekanisme keamanan, maupun materi lain yang dapat menimbulkan risiko privasi atau operasional. Bukti mentah disimpan terpisah dari laporan dan aksesnya dibatasi kepada anggota yang memerlukan.")


def add_chapter_4(doc):
    doc.add_page_break()
    doc.add_heading("BAB IV HASIL DAN PEMBAHASAN", level=1)
    add_body(doc, "Bab ini memisahkan fakta organisasi, hasil pemodelan, dan analisis tim. Sumber primer yang digunakan adalah wawancara dengan apt. Dirgan Yolanda, S.Farm., Kepala Ruangan/Penanggung Jawab Gudang Farmasi RS Unand, pada 29 September 2026. Transkrip telah dinormalisasi karena rekaman otomatis masih memuat kesalahan pengenalan istilah. Informasi yang belum jelas tetap ditandai untuk dikonfirmasi.")

    doc.add_heading("4.1 Preliminary Phase", level=2)
    doc.add_heading("4.1.1 Ruang Lingkup Organisasi", level=3)
    add_body(doc, "Ruang lingkup utama (core enterprise) ditetapkan pada fungsi Gudang Farmasi di dalam Instalasi Farmasi RS Unand, dengan fokus pada pengelolaan perbekalan farmasi. Pelayanan farmasi klinis tidak dianalisis secara rinci karena berhubungan langsung dengan pasien. Unit internal dan pihak luar dimasukkan hanya sejauh memiliki hubungan dengan pemilihan, perencanaan, pengadaan, penerimaan, penyimpanan, distribusi, pengendalian, penanganan kedaluwarsa/rusak, dan pelaporan.")
    add_table(
        doc,
        ["Kategori", "Pihak/unit", "Alasan keterlibatan", "Bukti"],
        [
            ("Core enterprise", "Gudang Farmasi/Instalasi Farmasi", "Objek utama pemetaan pengelolaan perbekalan", "Wawancara, 29 September 2026"),
            ("Soft enterprise", "Depo/apotek pelayanan, bagian pengadaan, keuangan, dan IT", "Permintaan, pengadaan, pelaporan, serta dukungan sistem", "Wawancara; rincian unit perlu dikonfirmasi"),
            ("Extended enterprise", "Distributor obat dan pihak ketiga pemusnahan", "Pemasokan barang dan pemusnahan barang kedaluwarsa/rusak", "Wawancara"),
            ("Communities involved", "Kementerian Kesehatan dan pihak regulator terkait", "Pelaporan eksternal dan kepatuhan", "Wawancara; [KONFIRMASI DAFTAR LENGKAP]"),
        ],
        widths=[3.5, 4, 6, 4],
        font_size=9,
        caption="Tabel 4.1 Ruang Lingkup Organisasi",
    )

    doc.add_heading("4.1.2 Tata Kelola dan Kewenangan", level=3)
    add_body(doc, "Menurut narasumber, Instalasi Farmasi berada di bawah Direktorat Pelayanan Medik dan Keperawatan melalui unsur Penunjang Medik. Di dalam instalasi terdapat Kepala Instalasi, Kepala Ruangan untuk pelayanan farmasi klinis dan pengelolaan perbekalan farmasi, penanggung jawab pada depo/apotek, serta staf pelaksana. Untuk kegiatan Gudang Farmasi, penanggung jawab melaporkan kepada Kepala Ruangan dan selanjutnya kepada Kepala Instalasi.")
    add_placeholder(doc, "Konfirmasikan nama jabatan formal, pejabat yang mengesahkan SOP, jalur persetujuan perubahan proses, dan posisi unsur Penunjang Medik berdasarkan dokumen organisasi terbaru.")
    add_source_note(doc, "Wawancara dengan apt. Dirgan Yolanda, S.Farm., 29 September 2026.")

    doc.add_heading("4.1.3 Tim Arsitek dan Tanggung Jawab", level=3)
    add_body(doc, "Tim arsitek terdiri atas enam mahasiswa sebagaimana Tabel Tim Arsitek pada BAB III. Ketua tim bertanggung jawab atas koordinasi, konsistensi keputusan, serta komunikasi resmi dengan pihak RS. Pembagian peran digunakan untuk memastikan proses, data/aplikasi, teknologi, kebutuhan, dan dokumentasi memperoleh perhatian yang memadai.")

    doc.add_heading("4.1.4 Architecture Principles", level=3)
    add_draft_note(doc, "Prinsip di bawah adalah kandidat awal, bukan prinsip resmi RS. Pertahankan, ubah, atau hapus berdasarkan visi–misi, regulasi, SOP, dan hasil wawancara.")
    add_table(
        doc,
        ["Kode", "Nama kandidat", "Pernyataan", "Rationale", "Implikasi", "Status validasi"],
        [
            ("AP-01", "Keselarasan dengan tujuan organisasi", "Perubahan proses dan sistem harus mendukung tujuan layanan dan tata kelola RS.", "Mencegah usulan yang tidak relevan dengan arah organisasi.", "Setiap rekomendasi harus ditelusuri ke tujuan/masalah yang sah.", "[VALIDASI]"),
            ("AP-02", "Kebenaran kondisi baseline", "Model AS-IS menggambarkan proses yang benar-benar berjalan.", "Gap analysis hanya sah jika titik awalnya akurat.", "Ketidakefisienan tetap dicatat; model diperiksa kembali oleh narasumber.", "[VALIDASI]"),
            ("AP-03", "Kerahasiaan dan kebutuhan minimum", "Data yang dikumpulkan dibatasi pada informasi yang diperlukan untuk tujuan arsitektur.", "Konteks rumah sakit memiliki risiko privasi tinggi.", "Data pasien dan konfigurasi keamanan tidak dikumpulkan; akses bukti dibatasi.", "[VALIDASI]"),
            ("AP-04", "Ketertelusuran", "Temuan, model, dan rekomendasi harus memiliki sumber yang dapat ditelusuri.", "Mengurangi risiko kesimpulan yang tidak didukung bukti.", "Sumber/penanda waktu dicatat dan analisis tim dibedakan dari fakta.", "[VALIDASI]"),
            ("AP-05", "Konsistensi istilah", "Nama proses, aktor, risiko, KPI, dan standar digunakan secara konsisten.", "Konsistensi dibutuhkan agar hubungan antarartefak dapat diperiksa.", "Daftar istilah disepakati dan dipakai di semua diagram/matriks.", "[VALIDASI]"),
        ],
        widths=[1.5, 3.5, 4, 4, 4, 2.5],
        font_size=8,
        caption="Tabel 4.2 Kandidat Architecture Principles",
    )

    doc.add_heading("4.1.5 Tailored Framework dan Tools", level=3)
    add_body(doc, "Metode disesuaikan dengan batas waktu dan tujuan akademik. Laporan kemajuan mengembangkan Preliminary Phase, Architecture Vision, dan Business Architecture. Pemodelan dilakukan di Sparx Enterprise Architect, sedangkan data sumber serta matriks kerja dipelihara dalam dokumen dan spreadsheet. Requirements Management berjalan sepanjang kegiatan melalui daftar pertanyaan, catatan kebutuhan, dan klarifikasi.")

    doc.add_heading("4.1.6 Ringkasan Preliminary Phase", level=3)
    add_table(
        doc,
        ["Langkah", "Keputusan/hasil", "Status"],
        [
            ("Menentukan lingkup organisasi", "Gudang Farmasi dalam Instalasi Farmasi dan proses pengelolaan perbekalan", "Terkonfirmasi melalui wawancara"),
            ("Menentukan governance", "Penanggung jawab Gudang Farmasi → Kepala Ruangan → Kepala Instalasi; jalur formal pengesahan SOP belum diperoleh", "Sebagian terkonfirmasi"),
            ("Membentuk tim EA", "Enam mahasiswa dengan pembagian peran", "Terkonfirmasi internal"),
            ("Menetapkan principles", "Lima kandidat prinsip", "Perlu validasi"),
            ("Tailoring TOGAF", "Preliminary dan Fase A–B untuk laporan kemajuan", "Terkonfirmasi dari format tugas"),
            ("Menentukan tools", "Sparx Enterprise Architect dan tools dokumentasi", "Terkonfirmasi internal"),
        ],
        widths=[5, 9, 4],
        font_size=9,
        caption="Tabel 4.3 Ringkasan Preliminary Phase",
    )

    doc.add_heading("4.2 Architecture Vision", level=2)
    doc.add_heading("4.2.1 Profil Singkat Organisasi", level=3)
    add_body(doc, "RS Unand merupakan Rumah Sakit Perguruan Tinggi Negeri di bawah pengelolaan Universitas Andalas dan berlokasi di Kompleks Kampus Universitas Andalas, Limau Manis, Padang. Menurut laman resminya, RS Unand mulai beroperasi pada 29 Maret 2017. Rumah sakit menjalankan pelayanan kesehatan, pendidikan, dan penelitian; instalasi farmasi tercantum sebagai salah satu layanan yang tersedia (RS Universitas Andalas, n.d.-a).")
    add_source_note(doc, "Laman Sejarah dan laman utama RS Universitas Andalas, diakses 29 September 2026.")

    doc.add_heading("4.2.2 Visi dan Misi Organisasi", level=3)
    add_body(doc, "Visi RS Unand adalah “Menjadi Rumah Sakit Pendidikan Terkemuka dan Bermartabat di Indonesia”. Misi organisasi meliputi pelayanan kesehatan berkualitas dan berbasis bukti, pendidikan profesi, penelitian kolaboratif dan translasional, pengembangan tata kelola rumah sakit pendidikan yang unggul serta adaptif, dan kerja sama produktif yang berkelanjutan (RS Universitas Andalas, n.d.-b).")
    add_source_note(doc, "Laman Visi & Misi RS Universitas Andalas, diakses 29 September 2026. Periksa kembali apabila RS memberikan dokumen versi lebih baru.")

    doc.add_heading("4.2.3 Pemangku Kepentingan dan Concern", level=3)
    add_body(doc, "Pemangku kepentingan awal diidentifikasi dari peran yang disebut selama wawancara. Concern utama yang muncul adalah ketersediaan barang, kesesuaian catatan sistem dengan kondisi fisik, ketertelusuran transaksi, ketepatan pelaporan, dan dukungan sistem terhadap pekerjaan manual. Daftar ini masih memerlukan pemeriksaan kepada unit lain karena wawancara utama dilakukan dari perspektif Gudang Farmasi.")
    add_table(
        doc,
        ["Stakeholder", "Peran", "Concern/kebutuhan", "Bukti", "Respons arsitektur"],
        [
            ("Kepala Instalasi Farmasi", "Pimpinan instalasi", "Kendali dan kepatuhan seluruh kegiatan kefarmasian", "Wawancara; nama belum diperoleh", "Tata kelola dan persetujuan"),
            ("Kepala Ruangan/Pj Gudang Farmasi", "Pengelola proses gudang", "Ketersediaan, akurasi stok, pelaporan, dan ketertelusuran", "Wawancara apt. Dirgan Yolanda, S.Farm.", "Baseline proses dan kebutuhan perbaikan"),
            ("Staf Gudang Farmasi", "Pelaksana", "Pencatatan sesuai tugas, kemudahan penggunaan sistem, dan investigasi selisih", "Wawancara", "Role, BPMN, dan kontrol proses"),
            ("Depo/apotek pelayanan", "Peminta/penerima distribusi", "Ketersediaan dan ketepatan serah terima barang", "Wawancara", "Proses distribusi"),
            ("Bagian pengadaan/distributor", "Pemesanan dan pemasok", "Kesesuaian pesanan, faktur, jumlah, batch, dan kedaluwarsa", "Wawancara", "Pengadaan dan penerimaan"),
            ("Bagian IT", "Pengelola teknis SIMRS", "Integritas transaksi, akses, integrasi, dan pengembangan fitur", "Belum diwawancarai", "[PERLU KONFIRMASI IT]"),
        ],
        widths=[3, 3, 4.5, 4, 4],
        font_size=8,
        caption="Tabel 4.4 Stakeholder dan Concern",
    )

    doc.add_heading("4.2.4 Architecture Goals", level=3)
    add_draft_note(doc, "Tujuan harus berasal dari tujuan organisasi dan temuan. Gunakan format terukur bila target resmi tersedia; jangan membuat angka target sendiri.")
    add_table(
        doc,
        ["Kode", "Tujuan arsitektur", "Dasar", "Ukuran keberhasilan", "Status"],
        [
            ("AG-01", "Menyediakan gambaran proses pengelolaan perbekalan farmasi yang konsisten dan dapat dipahami lintas peran.", "Ruang lingkup tugas dan kebutuhan dokumentasi", "Model tervalidasi; istilah konsisten", "Draf tim"),
            ("AG-02", "Meningkatkan keterlacakan perubahan stok dan transaksi dari penerimaan sampai distribusi.", "Risiko kehilangan/selisih dan kebutuhan investigasi", "Selisih dapat ditelusuri ke transaksi dan pengguna", "Draf berdasarkan wawancara"),
            ("AG-03", "Mengurangi pengolahan manual pada perencanaan dan pemantauan persediaan.", "Perhitungan kebutuhan, klasifikasi stok, dan VEN masih diolah manual", "[TARGET RESMI BELUM DIPEROLEH]", "Draf berdasarkan wawancara"),
            ("AG-04", "Meningkatkan keandalan pencatatan transaksi dan laporan persediaan.", "Keterangan mengenai keluaran harga dan transaksi ganda", "[UKURAN PERLU DISEPAKATI DENGAN FARMASI/IT]", "Perlu validasi teknis"),
        ],
        widths=[1.5, 7, 4, 4, 2.5],
        font_size=8,
        caption="Tabel 4.5 Architecture Goals",
    )

    doc.add_heading("4.2.5 Pernyataan Architecture Vision", level=3)
    add_draft_note(doc, "Rumusan awal: 'Terwujudnya pengelolaan perbekalan farmasi yang terdokumentasi, terkoordinasi, andal, dan dapat ditelusuri dari pemilihan hingga pelaporan untuk mendukung ketersediaan perbekalan serta tata kelola RS Unand.' Rumusan ini perlu dikonfirmasi kepada pihak RS.")

    doc.add_heading("4.2.6 Value Chain", level=3)
    add_body(doc, "Aktivitas utama yang diperoleh dari wawancara terdiri atas pemilihan, perencanaan, pengadaan, penerimaan, penyimpanan, distribusi, pengendalian, penanganan barang kedaluwarsa/rusak, dan pelaporan. Aktivitas pendukung mencakup pengelolaan SDM, anggaran, formularium dan SOP, dukungan SIMRS/RME, koordinasi dengan depo serta unit lain, dan hubungan dengan pemasok maupun pihak ketiga pemusnahan. Klasifikasi ini merupakan analisis awal tim dan harus digunakan secara konsisten pada BPMN serta Functional Decomposition.")
    add_figure_placeholder(doc, "Gambar 4.1 Value Chain Pengelolaan Perbekalan Farmasi", "Masukkan artefak hasil Sparx setelah daftar proses resmi ditetapkan.")

    doc.add_heading("4.2.7 Business Model Canvas", level=3)
    add_body(doc, "BMC pada ruang lingkup ini tidak dipakai untuk menggambarkan model bisnis komersial, melainkan konteks penciptaan nilai oleh pengelolaan perbekalan farmasi. Penerima nilai adalah unit pelayanan dan pasien secara tidak langsung; nilai yang didukung adalah ketersediaan perbekalan yang tepat, aman, dan dapat ditelusuri. Aktivitas utama mengikuti Value Chain, sedangkan sumber daya utama meliputi tenaga kefarmasian, anggaran pembelian, persediaan, fasilitas penyimpanan, serta SIMRS. Mitra utama mencakup unit internal, distributor, pihak ketiga pemusnahan, dan regulator.")
    add_figure_placeholder(doc, "Gambar 4.2 Business Model Canvas", "Masukkan artefak hasil Sparx.")

    doc.add_heading("4.2.8 Organization Decomposition", level=3)
    add_body(doc, "Berdasarkan wawancara, Instalasi Farmasi berada di bawah Direktorat Pelayanan Medik dan Keperawatan melalui unsur Penunjang Medik. Struktur internal yang disebut terdiri atas Kepala Instalasi, Kepala Ruangan pelayanan farmasi klinis, Kepala Ruangan pengelolaan perbekalan farmasi, penanggung jawab depo/apotek, dan staf. apt. Dirgan Yolanda, S.Farm. menjadi narasumber dalam kapasitas Kepala Ruangan/Penanggung Jawab Gudang Farmasi. Struktur formal harus dicocokkan dengan pedoman pengorganisasian RS sebelum diagram dinyatakan final.")
    add_draft_note(doc, "Catatan historis yang diinformasikan kepada tim menyebut dokumen RS Unand tahun 2022 mencantumkan apt. Dirgan Yolanda, S.Farm. sebagai anggota Komite Farmasi dan Terapi sekaligus Pj Gudang Farmasi. Informasi ini tidak digunakan sebagai jabatan terkini; judul dokumen, halaman, dan izin pencantumannya perlu dilengkapi sebelum dijadikan sitasi final.")
    add_figure_placeholder(doc, "Gambar 4.3 Organization Decomposition Diagram", "Masukkan artefak hasil Sparx dan sumber struktur organisasi.")

    doc.add_heading("4.3 Business Architecture", level=2)
    doc.add_heading("4.3.1 Gambaran Baseline", level=3)
    add_body(doc, "Pengelolaan perbekalan farmasi dimulai dari pemilihan obat berdasarkan formularium rumah sakit. Menurut narasumber, formularium ditinjau secara berkala dan dapat dilengkapi adendum. Usulan obat di luar formularium memerlukan pengajuan serta dokumen pendukung. Kebutuhan kemudian direncanakan menggunakan metode konsumsi berdasarkan pemakaian sebelumnya. Data konsumsi berasal dari SIMRS, tetapi perhitungannya masih diolah menggunakan Excel.")
    add_body(doc, "Pengadaan dilakukan melalui e-katalog atau pembelian langsung apabila barang tidak tersedia pada e-katalog. Ketika barang datang, petugas mencocokkan kondisi fisik dengan surat pesanan dan faktur, termasuk nama atau kekuatan, jumlah, nomor batch, dan tanggal kedaluwarsa. Kekurangan, kelebihan, atau ketidaksesuaian dicatat dan dikomunikasikan kepada distributor untuk dilengkapi atau dikembalikan.")
    add_body(doc, "Penyimpanan memperhatikan rentang suhu, pemisahan narkotika dan psikotropika, penggunaan palet, metode FEFO, serta penandaan obat high-alert dan LASA. Distribusi dimulai dari permintaan depo atau apotek, dilanjutkan penyiapan di gudang, pengantaran, dan serah terima. Stok opname internal dilakukan setiap tiga bulan dengan menghitung fisik sampai satuan terkecil, memeriksa kedaluwarsa, membandingkan hasil dengan SIMRS, dan menginvestigasi selisih.")
    add_body(doc, "SIMRS Transmedic mendukung pemesanan, penerimaan, kartu stok, distribusi, dan pelaporan persediaan. RME terintegrasi untuk mendukung resep elektronik. Meskipun demikian, klasifikasi fast moving, slow moving, dead stock, klasifikasi VEN, dan perhitungan kebutuhan masih dilakukan secara manual. Narasumber juga menyampaikan adanya kasus keluaran nilai harga yang tidak sesuai dan transaksi ganda setelah error dan pengulangan input. Temuan teknis tersebut perlu diverifikasi bersama bagian IT sebelum ditetapkan sebagai akar masalah sistem.")
    add_source_note(doc, "Wawancara dengan apt. Dirgan Yolanda, S.Farm., 29 September 2026.")

    doc.add_heading("4.3.2 Business Principles", level=3)
    add_body(doc, "Business Principles dirumuskan sebagai pedoman awal, yaitu kepatuhan pada formularium dan regulasi; ketertelusuran setiap transaksi; kesesuaian antara fisik dan catatan sistem; penerapan FEFO serta persyaratan penyimpanan; penggunaan akun individual sesuai kewenangan; dan pemisahan barang kedaluwarsa/rusak dari persediaan aktif. Setiap prinsip perlu dituangkan dalam format Name, Statement, Rationale, dan Implications serta divalidasi terhadap SOP internal.")
    add_draft_note(doc, "Daftar prinsip merupakan hasil analisis tim dari wawancara dan belum dinyatakan sebagai prinsip resmi RS Unand.")
    add_figure_placeholder(doc, "Gambar 4.4 Business Principles", "Masukkan artefak hasil Sparx.")

    doc.add_heading("4.3.3 Organization Role Diagram", level=3)
    add_body(doc, "Peran yang teridentifikasi meliputi Kepala Instalasi Farmasi, Kepala Ruangan/Penanggung Jawab Gudang Farmasi, petugas gudang, pejabat atau petugas pengadaan, penanggung jawab depo/apotek, staf pelayanan, distributor, serta bagian IT. Kepala Ruangan Gudang Farmasi mengoordinasikan kegiatan gudang; petugas menjalankan pencatatan sesuai akun dan kewenangan; bagian pengadaan merealisasikan pemesanan; sedangkan depo/apotek mengajukan permintaan dan menerima distribusi. Kewenangan formal setiap peran masih perlu dicocokkan dengan pedoman pengorganisasian dan SOP.")
    add_figure_placeholder(doc, "Gambar 4.5 Organization Role Diagram", "Masukkan artefak hasil Sparx.")

    doc.add_heading("4.3.4 Daftar Proses Resmi", level=3)
    add_body(doc, "Tabel ini menjadi kamus proses tunggal untuk seluruh artefak. Setelah disepakati, jangan mengganti nama proses pada satu diagram tanpa memperbarui seluruh matriks terkait.")
    add_table(
        doc,
        ["Kode", "Nama proses resmi", "Pemicu", "Aktor", "Output", "Sumber"],
        [
            ("BP-01", "Pemilihan", "Kebutuhan obat/formularium", "Instalasi Farmasi dan [KONFIRMASI PERAN KFT]", "Daftar obat yang dapat direncanakan", "Wawancara"),
            ("BP-02", "Perencanaan", "Data konsumsi dan kebutuhan layanan", "Petugas Gudang/Instalasi Farmasi", "Rencana kebutuhan", "Wawancara"),
            ("BP-03", "Pengadaan", "Rencana kebutuhan yang disetujui", "Pejabat/petugas pengadaan", "Surat pesanan", "Wawancara"),
            ("BP-04", "Penerimaan", "Barang dan dokumen dari distributor", "Petugas Gudang Farmasi", "Barang diterima atau berita acara ketidaksesuaian", "Wawancara"),
            ("BP-05", "Penyimpanan", "Barang yang lolos pemeriksaan", "Petugas Gudang Farmasi", "Barang tersimpan sesuai ketentuan", "Wawancara"),
            ("BP-06", "Distribusi", "Permintaan depo/apotek", "Petugas gudang dan petugas depo/apotek", "Barang diserahkan ke unit peminta", "Wawancara"),
            ("BP-07", "Pengendalian dan Stok Opname", "Jadwal tiga bulanan/data stok", "Petugas gudang dan penanggung jawab", "Hasil rekonsiliasi dan tindak lanjut selisih", "Wawancara"),
            ("BP-08", "Penanganan Kedaluwarsa/Rusak", "Temuan barang tidak layak digunakan", "Gudang, pimpinan, dan pihak ketiga", "Barang dipisahkan dan dimusnahkan", "Wawancara"),
            ("BP-09", "Pelaporan", "Data persediaan dan transaksi", "Gudang/Instalasi Farmasi", "Laporan internal dan eksternal", "Wawancara"),
        ],
        widths=[1.5, 4.5, 3, 3, 3, 4],
        font_size=8,
        caption="Tabel 4.6 Daftar Proses Resmi",
    )

    doc.add_heading("4.3.5 Business Process Diagram AS-IS", level=3)
    add_body(doc, "BPMN AS-IS disusun menggunakan sembilan proses pada daftar proses resmi. Model perlu menunjukkan lane untuk Gudang Farmasi, pihak pengadaan, depo/apotek, distributor, pimpinan terkait, dan pihak ketiga sejauh terlibat. Titik keputusan utama mencakup kesesuaian barang saat penerimaan, ketersediaan barang terhadap permintaan, selisih fisik dengan SIMRS, serta status barang kedaluwarsa/rusak.")
    add_placeholder(doc, "Masukkan BPMN AS-IS hasil Sparx setelah seluruh lane, gateway, dan urutan proses diperiksa bersama catatan wawancara.")
    add_figure_placeholder(doc, "Gambar 4.6 BPMN AS-IS Pengelolaan Perbekalan Farmasi", "Masukkan hasil ekspor Sparx dengan resolusi terbaca.")
    add_table(
        doc,
        ["Langkah", "Aktor", "Aktivitas/keputusan", "Input", "Output", "Sistem/media", "Bukti"],
        [
            ("1", "Instalasi Farmasi/[KFT]", "Memilih obat sesuai formularium dan menilai usulan baru", "Formularium/usulan", "Daftar terpilih", "Formulir dan dokumen", "Wawancara"),
            ("2", "Gudang/Instalasi Farmasi", "Mengolah kebutuhan dengan metode konsumsi", "Data konsumsi SIMRS", "Rencana kebutuhan", "SIMRS dan Excel", "Wawancara"),
            ("3", "Pejabat/petugas pengadaan", "Memesan melalui e-katalog atau pembelian langsung", "Rencana kebutuhan", "Surat pesanan", "E-katalog/SIMRS", "Wawancara"),
            ("4", "Petugas Gudang", "Memeriksa fisik, surat pesanan, faktur, batch, dan kedaluwarsa", "Barang dan dokumen", "Penerimaan/berita acara", "SIMRS dan dokumen", "Wawancara"),
            ("5", "Petugas Gudang", "Menyimpan sesuai suhu, FEFO, kategori, dan ketentuan khusus", "Barang diterima", "Persediaan tersimpan", "SIMRS/kartu stok", "Wawancara"),
            ("6", "Depo/apotek dan gudang", "Mengajukan, menyiapkan, mengantar, dan serah terima", "Permintaan unit", "Barang terdistribusi", "SIMRS", "Wawancara"),
            ("7", "Gudang/penanggung jawab", "Stok opname dan investigasi selisih", "Fisik dan stok sistem", "Rekonsiliasi/tindak lanjut", "SIMRS dan Excel", "Wawancara"),
            ("8", "Gudang/pimpinan/pihak ketiga", "Memisahkan, melaporkan, dan memusnahkan barang", "Barang kedaluwarsa/rusak", "Bukti penanganan", "Dokumen", "Wawancara"),
            ("9", "Gudang/Instalasi Farmasi", "Menyusun laporan internal dan eksternal", "Data transaksi/persediaan", "Laporan", "SIMRS, aplikasi eksternal, Google Form", "Wawancara"),
        ],
        widths=[1, 2.5, 4.5, 2.5, 2.5, 3, 3],
        font_size=8,
        caption="Tabel 4.7 Rincian Proses AS-IS",
    )

    doc.add_heading("4.3.6 Functional Decomposition Diagram", level=3)
    add_body(doc, "Fungsi pengelolaan perbekalan diuraikan menjadi sembilan fungsi tingkat pertama, yaitu pemilihan, perencanaan, pengadaan, penerimaan, penyimpanan, distribusi, pengendalian dan stok opname, penanganan kedaluwarsa/rusak, serta pelaporan. Subfungsi diturunkan dari langkah yang dijelaskan narasumber, misalnya pemeriksaan dokumen dan fisik pada penerimaan, pengaturan suhu dan FEFO pada penyimpanan, serta rekonsiliasi dan investigasi pada pengendalian stok.")
    add_placeholder(doc, "Masukkan Functional Decomposition Diagram hasil Sparx dan pastikan nama fungsi sama dengan BP-01 sampai BP-09.")
    add_figure_placeholder(doc, "Gambar 4.7 Functional Decomposition Diagram", "Masukkan artefak hasil Sparx.")

    doc.add_heading("4.3.7 Risiko", level=3)
    add_body(doc, "Risiko utama yang disebut narasumber adalah kehilangan atau selisih persediaan yang perlu ditelusuri melalui catatan transaksi. Risiko lain diturunkan secara hati-hati dari kendala dan kontrol yang dijelaskan. Risiko turunan tersebut masih merupakan analisis tim dan perlu divalidasi sebelum dinyatakan sebagai risiko resmi unit.")
    add_table(
        doc,
        ["Kode", "Risiko", "Penyebab", "Dampak", "Pengendalian saat ini", "Sumber"],
        [
            ("R-01", "Kehilangan atau selisih persediaan", "Perbedaan transaksi, pencatatan, atau kondisi fisik", "Stok tidak akurat dan investigasi tambahan", "Akun individual, kartu stok, stok opname, dan investigasi", "Wawancara"),
            ("R-02", "Transaksi tercatat ganda", "Pengulangan input setelah proses pertama error", "Catatan sistem berbeda dari pergerakan fisik", "Rekonsiliasi saat stok opname", "Wawancara; perlu verifikasi IT"),
            ("R-03", "Keluaran nilai harga tidak sesuai", "Penyebab teknis belum diketahui", "Laporan nilai persediaan/transaksi dapat tidak akurat", "Pemeriksaan laporan", "Wawancara; perlu verifikasi IT"),
            ("R-04", "Barang kedaluwarsa tidak tertangani tepat waktu", "Pemantauan masih memerlukan pengolahan manual", "Barang berisiko tidak dapat digunakan", "FEFO, pemeriksaan kedaluwarsa, pemisahan, dan pelaporan", "Analisis tim dari wawancara"),
        ],
        widths=[1.5, 4, 3.5, 3.5, 4, 3],
        font_size=8,
        caption="Tabel 4.8 Daftar Risiko",
    )
    add_figure_placeholder(doc, "Gambar 4.8 Risk Diagram", "Masukkan artefak hasil Sparx.")

    doc.add_heading("4.3.8 Key Performance Indicator", level=3)
    add_body(doc, "Wawancara belum menghasilkan indikator mutu proses Gudang Farmasi beserta definisi dan targetnya. Narasumber menjelaskan Indikator Kinerja Individu (IKI) yang diisi bulanan dan penilaian 360 derajat untuk evaluasi SDM. Keduanya merupakan penilaian personel dan tidak otomatis dapat digunakan sebagai KPI proses pengelolaan perbekalan. Oleh karena itu, KPI proses tetap ditandai untuk klarifikasi.")
    add_table(
        doc,
        ["Kode", "Indikator", "Definisi/cara ukur", "Target", "Periode", "Sumber"],
        [
            ("HR-01", "Indikator Kinerja Individu (IKI)", "Realisasi pekerjaan individu terhadap target personal", "Berbeda menurut pegawai; tidak diperoleh", "Bulanan", "Wawancara"),
            ("HR-02", "Penilaian 360 derajat", "Penilaian kinerja dari pihak yang berinteraksi", "Bersifat rahasia; tidak diperoleh", "[KONFIRMASI PERIODE]", "Wawancara"),
            ("KPI-01", "[INDIKATOR MUTU PROSES GUDANG]", "[DEFINISI/CARA UKUR]", "[TARGET RESMI]", "[PERIODE]", "[DOKUMEN/NARASUMBER]"),
        ],
        widths=[1.5, 4, 4.5, 3, 2.5, 3],
        font_size=8,
        caption="Tabel 4.9 Daftar Key Performance Indicator",
    )
    add_figure_placeholder(doc, "Gambar 4.9 KPI Diagram", "Masukkan artefak hasil Sparx.")

    doc.add_heading("4.3.9 Standard and Regulation", level=3)
    add_body(doc, "Permenkes Nomor 72 Tahun 2016 disebut oleh narasumber sebagai acuan utama. Judul dan statusnya telah diperiksa pada JDIH Kementerian Kesehatan, yaitu Peraturan Menteri Kesehatan Nomor 72 Tahun 2016 tentang Standar Pelayanan Kefarmasian di Rumah Sakit dan berstatus berlaku. Narasumber juga menyebut regulasi narkotika/psikotropika serta pedoman pelayanan dan pengorganisasian internal RS, tetapi nomor dan judul lengkapnya belum diperoleh.")
    add_table(
        doc,
        ["Kode", "Judul/nomor", "Penerbit", "Tahun/versi", "Proses terkait", "Bukti/status berlaku"],
        [
            ("SR-01", "Permenkes Nomor 72 Tahun 2016 tentang Standar Pelayanan Kefarmasian di Rumah Sakit", "Kementerian Kesehatan RI", "2016", "BP-01 sampai BP-09 sesuai relevansi", "JDIH Kemenkes; status berlaku"),
            ("SR-02", "[REGULASI NARKOTIKA/PSIKOTROPIKA YANG DIGUNAKAN UNIT]", "[PENERBIT]", "[TAHUN]", "Pemilihan, pengadaan, penyimpanan, distribusi, pelaporan", "[MINTA JUDUL/NOMOR PERSIS]"),
            ("SR-03", "[PEDOMAN PELAYANAN KEFARMASIAN RS UNAND]", "RS Unand", "[TAHUN/VERSI]", "Seluruh proses", "[MINTA DOKUMEN]"),
            ("SR-04", "[PEDOMAN PENGORGANISASIAN INSTALASI FARMASI]", "RS Unand", "[TAHUN/VERSI]", "Peran dan tata kelola", "[MINTA DOKUMEN]"),
        ],
        widths=[1.5, 5, 3, 2.5, 4, 4],
        font_size=8,
        caption="Tabel 4.10 Daftar Standard and Regulation",
    )
    add_figure_placeholder(doc, "Gambar 4.10 Standard and Regulation", "Masukkan artefak hasil Sparx.")

    doc.add_heading("4.3.10 Matriks Keterkaitan", level=3)
    add_body(doc, "Matriks disusun menggunakan kode yang sama dengan daftar proses, risiko, KPI, dan standar/regulasi. Tanda ✓ menunjukkan keterkaitan langsung berdasarkan wawancara atau analisis tim, sedangkan tanda – menunjukkan tidak ada hubungan langsung yang ditemukan pada data saat ini. Matriks yang memuat regulasi atau KPI belum dinyatakan final sebelum dokumen internal dan indikator proses diterima.")
    add_table(
        doc,
        ["Proses", "R-01", "R-02", "R-03", "R-04", "Alasan/keterangan"],
        [
            ("BP-01", "–", "–", "–", "✓", "Pemilihan memengaruhi jenis barang yang perlu dipantau masa berlakunya."),
            ("BP-02", "✓", "–", "–", "✓", "Ketepatan rencana memengaruhi ketersediaan, selisih, dan potensi kedaluwarsa."),
            ("BP-03", "✓", "–", "✓", "–", "Pesanan dan nilai transaksi menjadi dasar penerimaan serta pencatatan."),
            ("BP-04", "✓", "✓", "✓", "✓", "Penerimaan mencatat jumlah, harga, batch, dan tanggal kedaluwarsa."),
            ("BP-05", "✓", "–", "–", "✓", "Penyimpanan dan FEFO mengendalikan keberadaan serta masa berlaku barang."),
            ("BP-06", "✓", "✓", "✓", "–", "Distribusi mengubah stok dan dapat terpengaruh kesalahan transaksi atau nilai."),
            ("BP-07", "✓", "✓", "✓", "✓", "Stok opname mendeteksi selisih, transaksi ganda, nilai, dan kedaluwarsa."),
            ("BP-08", "✓", "–", "–", "✓", "Pemisahan dan pemusnahan mengubah jumlah persediaan dan menangani kedaluwarsa."),
            ("BP-09", "✓", "✓", "✓", "✓", "Pelaporan memakai keluaran seluruh transaksi dan hasil pengendalian."),
        ],
        widths=[2.2, 1.3, 1.3, 1.3, 1.3, 10.5],
        font_size=8,
        caption="Tabel 4.11 Business Process–Risk Matrix",
    )
    add_body(doc, "Business Process–KPI Matrix belum dapat diselesaikan secara sahih karena indikator mutu proses Gudang Farmasi, definisi operasional, target, dan periodenya belum diperoleh. IKI dan penilaian 360 derajat yang disebut narasumber merupakan penilaian personel, sehingga tidak dipaksakan sebagai KPI proses.")
    add_table(
        doc,
        ["Proses", "KPI proses", "Hubungan", "Alasan/keterangan"],
        [("BP-01 s.d. BP-09", "[KODE KPI RESMI]", "[✓/–]", "[ISI SETELAH DEFINISI, TARGET, PERIODE, DAN SUMBER KPI DIPEROLEH]")],
        widths=[4, 4, 2.5, 8],
        font_size=9,
        caption="Tabel 4.12 Business Process–KPI Matrix",
    )
    add_table(
        doc,
        ["Proses", "SR-01", "SR-02", "SR-03", "Alasan/keterangan"],
        [
            ("BP-01", "✓", "✓", "✓", "Pemilihan/formularium dan pengendalian obat khusus."),
            ("BP-02", "✓", "✓", "✓", "Perencanaan kebutuhan perbekalan."),
            ("BP-03", "✓", "✓", "✓", "Pengadaan dan pengendalian obat khusus."),
            ("BP-04", "✓", "✓", "✓", "Pemeriksaan penerimaan dan dokumen."),
            ("BP-05", "✓", "✓", "✓", "Penyimpanan umum dan penyimpanan khusus."),
            ("BP-06", "✓", "✓", "✓", "Distribusi umum dan obat khusus."),
            ("BP-07", "✓", "✓", "✓", "Pengendalian persediaan dan pencatatan."),
            ("BP-08", "✓", "✓", "✓", "Penanganan barang kedaluwarsa/rusak."),
            ("BP-09", "✓", "✓", "✓", "Pelaporan umum dan pelaporan obat khusus."),
        ],
        widths=[2.5, 2, 2, 2, 10.5],
        font_size=8,
        caption="Tabel 4.13 Business Process–Standard and Regulation Matrix",
    )
    add_draft_note(doc, "Kolom SR-02 dan SR-03 menunjukkan keterkaitan konseptual. Judul, nomor, versi, serta ketentuan rinci dokumennya tetap harus dikonfirmasi sebelum matriks difinalkan.")

    doc.add_heading("4.3.11 Business Interaction Matrix", level=3)
    add_body(doc, "Matriks berikut memetakan interaksi operasional yang dijelaskan dalam wawancara. R berarti menjalankan aktivitas, A berarti bertanggung jawab atau memberi persetujuan, C berarti dikonsultasikan/berkoordinasi, dan I berarti menerima informasi. Penetapan A masih bersifat draf karena dokumen kewenangan formal belum diperoleh.")
    add_table(
        doc,
        ["Proses", "Instalasi/Ka. Ruang", "Gudang", "Pengadaan", "Depo/apotek", "Distributor/pihak ketiga", "Keterangan"],
        [
            ("BP-01 Pemilihan", "R/A", "C", "I", "C", "I", "Melibatkan formularium; peran KFT perlu dikonfirmasi."),
            ("BP-02 Perencanaan", "A", "R", "C", "C", "I", "Data konsumsi diolah menjadi rencana kebutuhan."),
            ("BP-03 Pengadaan", "A/C", "C", "R", "I", "C", "Melalui e-katalog atau pembelian langsung."),
            ("BP-04 Penerimaan", "A", "R", "C", "I", "C", "Gudang memeriksa barang dan dokumen."),
            ("BP-05 Penyimpanan", "A", "R", "I", "I", "–", "Gudang menerapkan ketentuan penyimpanan dan FEFO."),
            ("BP-06 Distribusi", "A", "R", "I", "R/C", "–", "Depo/apotek meminta dan menerima barang."),
            ("BP-07 Pengendalian", "A", "R", "I", "C", "–", "Gudang melakukan stok opname dan investigasi."),
            ("BP-08 Kedaluwarsa/rusak", "A", "R", "C/I", "I", "R/C", "Pihak ketiga berizin menangani pemusnahan."),
            ("BP-09 Pelaporan", "A", "R", "C/I", "I", "I", "Gudang/instalasi menyusun laporan."),
        ],
        widths=[3.2, 2.6, 1.7, 2, 2.2, 3, 5],
        font_size=7,
        caption="Tabel 4.14 Business Interaction Matrix",
    )
    add_draft_note(doc, "Validasi kode A dan kewenangan persetujuan dengan pedoman pengorganisasian, SOP, atau konfirmasi Kepala Instalasi Farmasi.")

    doc.add_heading("4.3.12 Permasalahan Prioritas", level=3)
    add_body(doc, "Tiga masalah dipilih berdasarkan keterkaitannya dengan akurasi persediaan, beban kerja, dan kesinambungan pelayanan. Penyebab teknis tidak disimpulkan hanya dari satu wawancara; bagian yang belum dikonfirmasi dinyatakan secara terbuka.")
    add_table(
        doc,
        ["Kode", "Masalah", "Bukti", "Penyebab yang terkonfirmasi", "Dampak", "Prioritas/alasan"],
        [
            ("M-01", "Keandalan sebagian keluaran transaksi belum konsisten", "Narasumber menyebut nilai harga yang tidak sesuai dan transaksi ganda setelah error serta input ulang", "Kejadian telah dijelaskan; akar teknis belum dikonfirmasi bagian IT", "Catatan stok atau nilai transaksi berpotensi berbeda dan memerlukan rekonsiliasi", "Tinggi; berkaitan langsung dengan integritas data dan pelaporan"),
            ("M-02", "Perencanaan dan analisis persediaan masih memerlukan pengolahan manual", "Perhitungan kebutuhan, fast/slow/dead stock, dan VEN diolah di Excel/manual", "Fungsi analitik tersebut belum sepenuhnya tersedia atau dimanfaatkan dalam SIMRS menurut narasumber", "Waktu pengolahan bertambah dan hasil bergantung pada ketelitian pengolah", "Tinggi; berulang dan memengaruhi keputusan persediaan"),
            ("M-03", "Pemantauan stok, batch, dan kedaluwarsa belum sepenuhnya proaktif", "Harapan narasumber mencakup peringatan stok minimum serta ketertelusuran batch/kedaluwarsa", "Ketersediaan fitur dan konfigurasinya belum diverifikasi kepada IT", "Risiko kekurangan, kedaluwarsa, atau penelusuran yang lambat", "Menengah–tinggi; berdampak pada ketersediaan dan keselamatan pengelolaan"),
        ],
        widths=[1.2, 3.6, 4, 4, 3.5, 3.5],
        font_size=7,
        caption="Tabel 4.15 Permasalahan Prioritas",
    )

    doc.add_heading("4.3.13 Business Process Diagram TO-BE", level=3)
    add_draft_note(doc, "TO-BE adalah usulan akademik tim. Setiap perubahan harus menanggapi masalah yang terkonfirmasi dan merujuk pada Architecture Goals/Principles. Jangan menyatakan bahwa RS telah menyetujui implementasi kecuali ada bukti tertulis.")
    add_body(doc, "Rancangan TO-BE mempertahankan sembilan proses utama dan kontrol yang telah berjalan, termasuk pemeriksaan penerimaan, FEFO, akun individual, stok opname tiga bulanan, serta pemisahan barang kedaluwarsa/rusak. Perubahan diarahkan pada titik yang ditemukan bermasalah, bukan mengganti seluruh alur.")
    add_body(doc, "Pada perencanaan, data konsumsi dari SIMRS diusulkan dapat diolah menjadi rekomendasi kebutuhan dan klasifikasi fast moving, slow moving, dead stock, serta VEN yang tetap ditinjau petugas. Pada pencatatan transaksi, sistem diusulkan melakukan validasi sebelum penyimpanan, menampilkan status berhasil/gagal dengan jelas, mencegah penyimpanan ulang atas transaksi yang sama, dan menyediakan jejak perubahan untuk investigasi.")
    add_body(doc, "Pada pengendalian persediaan, dashboard atau laporan kerja diusulkan menampilkan stok minimum, batch, tanggal kedaluwarsa, dan selisih hasil rekonsiliasi. Peringatan tidak menggantikan pemeriksaan fisik dan keputusan petugas. Kebutuhan, kelayakan teknis, kewenangan akses, serta integrasi usulan tersebut harus divalidasi bersama Instalasi Farmasi dan bagian IT.")
    add_figure_placeholder(doc, "Gambar 4.11 BPMN TO-BE Pengelolaan Perbekalan Farmasi", "Duplikasi AS-IS, modifikasi hanya bagian yang memiliki alasan, dan tandai aktivitas baru/berubah.")

    doc.add_heading("4.3.14 Gap Analysis dan Rekomendasi", level=3)
    add_table(
        doc,
        ["Kode", "Baseline", "Target", "Gap", "Tindakan", "Dasar", "Rekomendasi"],
        [
            ("G-01", "Kebutuhan dan klasifikasi persediaan diolah manual dari data SIMRS", "Sistem menyajikan olahan awal yang dapat diperiksa petugas", "Belum ada dukungan analitik terintegrasi yang terkonfirmasi", "Add/Modify", "M-02; AG-03; AP-02", "Analisis kebutuhan fitur bersama farmasi dan IT; mulai dari laporan terstruktur sebelum otomatisasi penuh"),
            ("G-02", "Pernah terjadi nilai harga tidak sesuai dan transaksi ganda setelah pengulangan input", "Setiap transaksi tervalidasi, berstatus jelas, tidak tersimpan ganda, dan dapat ditelusuri", "Kontrol transaksi dan akar teknis belum diketahui", "Modify", "M-01; R-02; R-03; AG-04", "Verifikasi log dan skenario error bersama IT, lalu tetapkan validasi, pencegahan duplikasi, dan audit trail"),
            ("G-03", "Pemantauan stok minimum, batch, dan kedaluwarsa belum sepenuhnya proaktif", "Peringatan dan daftar prioritas tersedia sesuai kewenangan", "Fitur/keterpakaian peringatan belum terkonfirmasi", "Add", "M-03; R-04; AG-02", "Uji kebutuhan peringatan stok minimum dan kedaluwarsa serta penelusuran batch tanpa menghilangkan FEFO fisik"),
            ("G-04", "Stok opname fisik dilakukan setiap tiga bulan dan selisih diinvestigasi", "Kontrol fisik tetap berjalan dengan dukungan rekonsiliasi yang mudah ditelusuri", "Ringkasan selisih dan hubungan ke transaksi masih dapat diperkuat", "Keep/Add", "R-01; AG-02; AP-03", "Pertahankan stok opname; tambahkan ringkasan selisih, referensi transaksi, pengguna, waktu, dan tindak lanjut"),
        ],
        widths=[1.2, 3.3, 3.3, 3.3, 2.2, 3, 4.5],
        font_size=6.8,
        caption="Tabel 4.16 Gap Analysis dan Rekomendasi",
    )
    add_body(doc, "Rekomendasi pada laporan kemajuan dibatasi pada arah perbaikan. Jadwal implementasi rinci, anggaran solusi, pengadaan, dan roadmap migrasi tidak disusun sebagai komitmen karena berada di luar fase yang dikerjakan.")


def add_references_and_appendices(doc):
    doc.add_page_break()
    doc.add_heading("DAFTAR REFERENSI", level=1)
    refs = [
        "Adenuga, O. A., Kekwaletswe, R. M., & Coleman, A. (2015). eHealth integration and interoperability issues: towards a solution through enterprise architecture. Health Information Science and Systems, 3, Article 1. https://doi.org/10.1186/s13755-015-0009-7",
        "Gong, Y., & Janssen, M. (2019). The value of and myths about enterprise architecture. International Journal of Information Management, 46, 1–9. https://doi.org/10.1016/j.ijinfomgt.2018.11.006",
        "Hazen, B. T., Bradley, R. V., Bell, J. E., In, J., & Byrd, T. A. (2017). Enterprise architecture: A competence-based approach to achieving agility and firm performance. International Journal of Production Economics, 193, 566–577. https://doi.org/10.1016/j.ijpe.2017.08.022",
        "ISO/IEC/IEEE. (2022). ISO/IEC/IEEE 42010:2022 Software, systems and enterprise—Architecture description. International Organization for Standardization. https://www.iso.org/standard/74393.html",
        "Kementerian Kesehatan Republik Indonesia. (2016). Peraturan Menteri Kesehatan Republik Indonesia Nomor 72 Tahun 2016 tentang Standar Pelayanan Kefarmasian di Rumah Sakit. JDIH Kementerian Kesehatan Republik Indonesia. https://jdih.kemkes.go.id/documents/peraturan-menteri-kesehatan-nomor-72-tahun-2016",
        "Object Management Group. (2014). Business Process Model and Notation (BPMN), Version 2.0.2. https://www.omg.org/spec/BPMN/2.0.2/PDF",
        "RS Universitas Andalas. (n.d.-a). Sejarah. Retrieved September 29, 2026, from https://rsp.unand.ac.id/sejarah",
        "RS Universitas Andalas. (n.d.-b). Visi & Misi. Retrieved September 29, 2026, from https://rsp.unand.ac.id/visi-misi",
        "Shanks, G., Gloet, M., Someh, I. A., Frampton, K., & Tamm, T. (2018). Achieving benefits with enterprise architecture. The Journal of Strategic Information Systems, 27(2), 139–156. https://doi.org/10.1016/j.jsis.2018.03.001",
        "Tamm, T., Seddon, P. B., Shanks, G., & Reynolds, P. (2011). How does enterprise architecture add value to organisations? Communications of the Association for Information Systems, 28, 141–168. https://doi.org/10.17705/1CAIS.02810",
        "Tamm, T., Seddon, P. B., & Shanks, G. (2022). How enterprise architecture leads to organisational benefits. International Journal of Information Management, 67, Article 102554. https://doi.org/10.1016/j.ijinfomgt.2022.102554",
        "The Open Group. (2018). The TOGAF Standard, Version 9.2 (Document C182). The Open Group. ISBN 1-947754-11-9. https://www.opengroup.org/togaf-standard-version-92-overview",
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Cm(1.27)
        p.paragraph_format.first_line_indent = Cm(-1.27)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(6)
        p.add_run(ref)

    doc.add_page_break()
    doc.add_heading("LAMPIRAN A\nINSTRUMEN WAWANCARA", level=1)
    add_placeholder(doc, "Masukkan daftar data dan 36 pertanyaan wawancara versi terbaru. Pastikan nomor pertanyaan sama dengan catatan dan transkrip.")

    doc.add_page_break()
    doc.add_heading("LAMPIRAN B\nDOKUMENTASI OBSERVASI/WAWANCARA", level=1)
    add_placeholder(doc, "Masukkan foto yang telah mendapat izin. Beri keterangan tanggal, lokasi, kegiatan, dan pihak yang tampak. Periksa ulang agar tidak ada data pasien, resep, layar sistem sensitif, dokumen harga, atau wajah pasien/pengunjung.")
    for i in range(1, 5):
        add_figure_placeholder(doc, f"Gambar B.{i} [ISI KETERANGAN FOTO]", "Masukkan foto dokumentasi yang aman.")

    doc.add_page_break()
    doc.add_heading("LAMPIRAN C\nRINGKASAN WAWANCARA", level=1)
    add_table(
        doc,
        ["Keterangan", "Isi"],
        [
            ("Tanggal/waktu", "29 September 2026; [ISI JAM/DURASI]"),
            ("Lokasi", "Gudang Farmasi, Instalasi Farmasi, Rumah Sakit Universitas Andalas"),
            ("Narasumber/jabatan", "apt. Dirgan Yolanda, S.Farm. — Kepala Ruangan/Penanggung Jawab Gudang Farmasi"),
            ("Pewawancara/pencatat", "[ISI]"),
            ("Izin rekaman/foto", "[ISI]"),
        ],
        widths=[5, 11],
    )
    add_body(doc, "Ringkasan hasil wawancara: pengelolaan perbekalan mencakup pemilihan, perencanaan, pengadaan, penerimaan, penyimpanan, distribusi, pengendalian, penanganan kedaluwarsa/rusak, dan pelaporan. SIMRS Transmedic mendukung transaksi utama, sedangkan perencanaan kebutuhan serta beberapa analisis persediaan masih diolah menggunakan Excel atau secara manual. Kontrol yang dijelaskan meliputi pemeriksaan dokumen dan fisik saat penerimaan, FEFO, pengaturan penyimpanan, akun individual, serta stok opname tiga bulanan. Kendala yang perlu diverifikasi bersama IT adalah keluaran nilai harga yang tidak sesuai dan transaksi ganda setelah error serta pengulangan input. Narasumber mengharapkan dukungan pemantauan stok minimum dan ketertelusuran batch/kedaluwarsa yang lebih baik.")
    add_source_note(doc, "Ringkasan terverifikasi sementara dari catatan dan transkrip wawancara, 29 September 2026. Kalimat diperbaiki untuk keterbacaan tanpa mengubah substansi jawaban.")
    add_placeholder(doc, "Lampirkan transkrip final hanya setelah nama pembicara, penanda waktu, dan bagian yang tidak terdengar diperiksa. Hapus nomor telepon serta data pribadi/sensitif yang tidak relevan.")

    doc.add_page_break()
    doc.add_heading("LAMPIRAN D\nDAFTAR DOKUMEN PENDUKUNG", level=1)
    add_table(
        doc,
        ["No.", "Dokumen", "Sumber/pemilik", "Tanggal/versi", "Izin penggunaan", "Digunakan pada"],
        [
            ("1", "Catatan dan transkrip wawancara Gudang Farmasi", "Tim EA / apt. Dirgan Yolanda, S.Farm.", "29 September 2026", "[KONFIRMASI IZIN PENCANTUMAN]", "BAB III, BAB IV, Lampiran C"),
            ("2", "Permenkes Nomor 72 Tahun 2016", "JDIH Kementerian Kesehatan RI", "2016; status berlaku saat diperiksa", "Dokumen publik", "Subbab 4.3.9 dan matriks"),
            ("3", "[DOKUMEN RS UNAND TAHUN 2022 YANG MEMUAT PENUGASAN NARASUMBER]", "RS Universitas Andalas", "2022", "[KONFIRMASI JUDUL, HALAMAN, DAN IZIN]", "[JIKA DIGUNAKAN]"),
        ],
        widths=[1, 4.5, 3.5, 3, 3.5, 3.5],
        font_size=8,
    )

    doc.add_page_break()
    doc.add_heading("LAMPIRAN E\nMATRIKS KETERTELUSURAN", level=1)
    add_body(doc, "Matriks ini digunakan untuk memeriksa bahwa setiap klaim dan rekomendasi memiliki dasar yang dapat ditelusuri.")
    add_table(
        doc,
        ["ID", "Pernyataan/temuan", "Jenis", "Sumber", "Lokasi sumber", "Dipakai pada"],
        [
            ("EV-01", "RS Unand merupakan RSPTN di bawah pengelolaan Universitas Andalas", "Fakta publik", "Laman resmi RS Unand", "Sejarah/laman utama", "BAB I dan 4.2"),
            ("EV-02", "Visi dan misi RS Unand", "Fakta publik", "Laman resmi RS Unand", "Visi & Misi", "BAB I dan 4.2"),
            ("EV-03", "Alur pengelolaan perbekalan, kontrol, penggunaan SIMRS/Excel, dan kendala operasional", "Fakta primer", "Wawancara apt. Dirgan Yolanda, S.Farm.", "Catatan/transkrip 29 September 2026", "Subbab 4.1–4.3"),
            ("EV-04", "Permenkes Nomor 72 Tahun 2016 berjudul Standar Pelayanan Kefarmasian di Rumah Sakit dan berstatus berlaku", "Fakta regulasi", "JDIH Kementerian Kesehatan RI", "Halaman metadata peraturan", "Subbab 4.3.9"),
            ("AN-01", "Masalah prioritas, target TO-BE, serta gap dan rekomendasi", "Analisis tim", "EV-03 + R-01 s.d. R-04 + AG-02 s.d. AG-04", "Subbab 4.3.12–4.3.14", "Tabel 4.15–4.16"),
        ],
        widths=[1.5, 5, 2.5, 4, 4, 3],
        font_size=8,
    )


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    configure_document(doc)
    set_update_fields(doc)
    add_cover(doc)
    add_approval(doc)
    add_front_matter(doc)
    add_chapter_1(doc)
    add_chapter_2(doc)
    add_chapter_3(doc)
    add_chapter_4(doc)
    add_references_and_appendices(doc)
    apply_chapter_styles(doc)
    force_times_new_roman(doc)

    props = doc.core_properties
    props.title = "Laporan Kemajuan Enterprise Architecture — Instalasi Farmasi RS Universitas Andalas"
    props.subject = "Tugas Besar Enterprise Architecture menggunakan TOGAF 9.2"
    props.author = "Kelompok 4 — Program Studi Sistem Informasi Universitas Andalas"
    props.keywords = "Enterprise Architecture, TOGAF 9.2, Business Architecture, RS Universitas Andalas, Instalasi Farmasi"
    props.comments = "Draf pascawawancara Kelompok 4; seluruh placeholder berwarna wajib diverifikasi dan diganti sebelum finalisasi."

    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
