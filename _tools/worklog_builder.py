"""
Builds a filled-in COS30018 "LAB Work Log" (.docx) from the official template
("Lab Worklog Template.docx" in the repo root), so the Swinburne header/logo,
footer and table styling stay exactly the same as the template.

You normally don't run this directly - run build_worklogs.py instead:

    python _tools/build_worklogs.py          # rebuild all weeks
    python _tools/build_worklogs.py 8        # rebuild only week 8

WARNING: rebuilding overwrites the worklog .docx for that week, so any edits
you made by hand in Word (or screenshots you pasted in) would be lost.
To add screenshots without rebuilding, use insert_screenshots.py instead.
"""

import copy
import datetime
import os

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.table import Table
from docx.text.paragraph import Paragraph

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(REPO_ROOT, "Lab Worklog Template.docx")

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14_NS = "http://schemas.microsoft.com/office/word/2010/wordml"

FONT = "Arial"
HEADER_FILL = "DEEAF6"      # same light blue as the template header cells
PLACEHOLDER_FILL = "FFF2CC"  # light yellow for "screenshot goes here" boxes
DONE_COLOUR = RGBColor(0x37, 0x86, 0x3C)
TODO_COLOUR = RGBColor(0xC0, 0x50, 0x00)


# --------------------------------------------------------------------------
# small formatting helpers
# --------------------------------------------------------------------------
# OOXML schema order of child elements - Word (unlike LibreOffice) can refuse to
# open a file whose elements are out of order, so always insert in the right spot
TBLPR_ORDER = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize",
               "tblStyleColBandSize", "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders",
               "shd", "tblLayout", "tblCellMar", "tblLook", "tblCaption", "tblDescription"]
TCPR_ORDER = ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd", "noWrap",
              "tcMar", "textDirection", "tcFitText", "vAlign", "hideMark"]


def _insert_ordered(parent, child, order):
    """Insert `child` into `parent` respecting the schema `order` (local names)."""
    name = child.tag.split("}")[1]
    for old in parent.findall(child.tag):
        parent.remove(old)
    later = order[order.index(name) + 1:]
    for i, sib in enumerate(parent):
        if sib.tag.split("}")[1] in later:
            parent.insert(i, child)
            return child
    parent.append(child)
    return child


def _strip_ids(el):
    """Remove w14:paraId / w14:textId so copied elements don't clash."""
    for node in el.iter():
        for attr in (f"{{{W14_NS}}}paraId", f"{{{W14_NS}}}textId"):
            if attr in node.attrib:
                del node.attrib[attr]


def _style_run(run, bold=False, italic=False, size=10, colour=None,
               highlight=None, font=FONT, mono=False):
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    name = "Consolas" if mono else font
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(a), name)
    if colour is not None:
        run.font.color.rgb = colour
    if highlight:
        hl = OxmlElement("w:highlight")
        hl.set(qn("w:val"), highlight)
        rpr.append(hl)
    return run


def _add_rich_text(paragraph, text, size=10, base_bold=False, italic=False,
                   colour=None):
    """Very small markup: **bold** and `code` inside a string."""
    import re
    tokens = re.split(r"(\*\*.+?\*\*|`.+?`)", text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            _style_run(paragraph.add_run(tok[2:-2]), bold=True, italic=italic,
                       size=size, colour=colour)
        elif tok.startswith("`") and tok.endswith("`"):
            _style_run(paragraph.add_run(tok[1:-1]), bold=base_bold,
                       italic=italic, size=size - 0.5, colour=colour, mono=True)
        else:
            _style_run(paragraph.add_run(tok), bold=base_bold, italic=italic,
                       size=size, colour=colour)
    return paragraph


def _set_spacing(paragraph, before=0, after=60, line=None):
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line:
        pf.line_spacing = line


def _make_bullet(paragraph):
    """Use the template's own bullet list (numId 1 = '•')."""
    ppr = paragraph._p.get_or_add_pPr()
    pstyle = OxmlElement("w:pStyle")
    pstyle.set(qn("w:val"), "ListParagraph")
    ppr.insert(0, pstyle)
    numpr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    numid = OxmlElement("w:numId")
    numid.set(qn("w:val"), "1")
    numpr.append(ilvl)
    numpr.append(numid)
    ppr.append(numpr)


def _shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    _insert_ordered(tcpr, shd, TCPR_ORDER)


def _cell_width(cell, twips):
    tcpr = cell._tc.get_or_add_tcPr()
    tcw = tcpr.find(qn("w:tcW"))
    if tcw is None:
        tcw = _insert_ordered(tcpr, OxmlElement("w:tcW"), TCPR_ORDER)
    tcw.set(qn("w:w"), str(twips))
    tcw.set(qn("w:type"), "dxa")


def _table_borders(table, val="single", colour="808080", sz=4):
    tblpr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), val)
        b.set(qn("w:sz"), str(sz))
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), colour)
        borders.append(b)
    _insert_ordered(tblpr, borders, TBLPR_ORDER)


def _table_width(table, twips, grid):
    tblpr = table._tbl.tblPr
    tblw = tblpr.find(qn("w:tblW"))
    if tblw is None:
        tblw = _insert_ordered(tblpr, OxmlElement("w:tblW"), TBLPR_ORDER)
    tblw.set(qn("w:w"), str(twips))
    tblw.set(qn("w:type"), "dxa")
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    _insert_ordered(tblpr, layout, TBLPR_ORDER)
    tblgrid = table._tbl.tblGrid
    for gc, w in zip(tblgrid.findall(qn("w:gridCol")), grid):
        gc.set(qn("w:w"), str(w))


def _clear_cell(cell):
    for p in list(cell.paragraphs):
        p._p.getparent().remove(p._p)


def _checkbox_sdt(checked):
    """A real clickable Word checkbox (content control)."""
    glyph = "☒" if checked else "☐"
    return parse_xml(
        f'<w:sdt xmlns:w="{W_NS}" xmlns:w14="{W14_NS}">'
        "<w:sdtPr>"
        '<w:rPr><w:rFonts w:ascii="MS Gothic" w:eastAsia="MS Gothic" w:hAnsi="MS Gothic"/>'
        '<w:sz w:val="22"/></w:rPr>'
        "<w14:checkbox>"
        f'<w14:checked w14:val="{1 if checked else 0}"/>'
        '<w14:checkedState w14:val="2612" w14:font="MS Gothic"/>'
        '<w14:uncheckedState w14:val="2610" w14:font="MS Gothic"/>'
        "</w14:checkbox>"
        "</w:sdtPr>"
        "<w:sdtContent>"
        '<w:r><w:rPr><w:rFonts w:ascii="MS Gothic" w:eastAsia="MS Gothic" w:hAnsi="MS Gothic"/>'
        f'<w:sz w:val="22"/></w:rPr><w:t>{glyph}</w:t></w:r>'
        "</w:sdtContent>"
        "</w:sdt>"
    )


def _new_paragraph_after(anchor_el, parent):
    p = OxmlElement("w:p")
    anchor_el.addnext(p)
    return Paragraph(p, parent)


def _new_table_after(doc, anchor_el, rows, cols):
    table = doc.add_table(rows=rows, cols=cols)
    table.style = doc.tables[0].style  # "Table Grid" like the template
    anchor_el.addnext(table._tbl)
    return table


# --------------------------------------------------------------------------
# the actual builder
# --------------------------------------------------------------------------
def build_worklog(spec, out_path):
    """
    spec = {
      "week": 5, "dates": "10-16 September 2026",
      "student_name": "...", "student_id": "...",
      "title": "Week 5 - Python, Google Colab, sklearn & Linear Regression",
      "checklist": [("item text", True/False), ...],
      "rows": [{"task": "...", "task_note": "...", "did": [...], "time": "1 h",
                "learning": [...], "problems": [...]}, ...],
      "total_time": "6.5 h",
      "figures": [{"path": "abs path", "caption": "...", "width": 6.0}, ...],
      "screenshots": [{"id": "5.1", "title": "...", "what": "...",
                       "file": "screenshots/5.1_xxx.png"}, ...],
      "notes": ["optional extra paragraph", ...],
    }
    """
    doc = Document(TEMPLATE)
    body = doc.element.body
    ident, main = doc.tables[0], doc.tables[1]

    # ---- 1. identity table -------------------------------------------------
    values = [
        (str(spec["week"]), False),
        (spec.get("student_name") or "[YOUR FULL NAME]",
         not spec.get("student_name")),
        (spec.get("student_id") or "[YOUR STUDENT ID]",
         not spec.get("student_id")),
    ]
    for row, (val, is_placeholder) in zip(ident.rows, values):
        cell = row.cells[1]
        p = cell.paragraphs[0]
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
        _style_run(p.add_run(val), bold=True, size=10,
                   highlight="yellow" if is_placeholder else None)

    # ---- 2. title + checklist right after the identity table ---------------
    anchor = ident._tbl
    title_p = _new_paragraph_after(anchor, doc._body)
    _set_spacing(title_p, before=10, after=4)
    _style_run(title_p.add_run(spec["title"]), bold=True, size=12)
    anchor = title_p._p

    if spec.get("intro"):
        intro_p = _new_paragraph_after(anchor, doc._body)
        _set_spacing(intro_p, before=0, after=6)
        _add_rich_text(intro_p, spec["intro"], size=9.5, italic=True)
        anchor = intro_p._p

    checklist = spec["checklist"]
    tbl = _new_table_after(doc, anchor, rows=len(checklist) + 1, cols=3)
    _table_borders(tbl)
    _table_width(tbl, 8965, [520, 7045, 1400])
    head = tbl.rows[0].cells
    merged = head[0].merge(head[1])   # merge BEFORE clearing (python-docx needs content)
    for c in (merged, head[2]):
        _shade(c, HEADER_FILL)
        _clear_cell(c)
    hp = merged.add_paragraph()
    _set_spacing(hp, before=3, after=3)
    _style_run(hp.add_run(f"LAB {spec['week']} CHECKLIST  "), bold=True)
    _style_run(hp.add_run("(☒ = done, ☐ = still to do)"),
               italic=True, size=8.5)
    sp = head[2].add_paragraph()
    sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _set_spacing(sp, before=3, after=3)
    _style_run(sp.add_run("STATUS"), bold=True)
    n_done = 0
    for row, (text, done) in zip(tbl.rows[1:], checklist):
        n_done += bool(done)
        c0, c1, c2 = row.cells
        for c in (c0, c1, c2):
            _clear_cell(c)
        p0 = c0.add_paragraph()
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _set_spacing(p0, before=1, after=1)
        p0._p.append(_checkbox_sdt(done))
        p1 = c1.add_paragraph()
        _set_spacing(p1, before=2, after=2)
        _add_rich_text(p1, text, size=9)
        p2 = c2.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _set_spacing(p2, before=2, after=2)
        _style_run(p2.add_run("Done" if done else "To do"), bold=True, size=9,
                   colour=DONE_COLOUR if done else TODO_COLOUR)
    progress_p = _new_paragraph_after(tbl._tbl, doc._body)
    _set_spacing(progress_p, before=3, after=0)
    _style_run(progress_p.add_run(
        f"Progress: {n_done}/{len(checklist)} items done"), italic=True,
        size=8.5)

    # ---- 3. main week table -------------------------------------------------
    week_cell = main.rows[0].cells[1]
    for p in week_cell.paragraphs:
        for r in p.runs:
            if r.text.strip() == "6":
                r.text = str(spec["week"])
    dates_cell = main.rows[1].cells[1]
    dp = dates_cell.paragraphs[0]
    for r in list(dp.runs):
        r._r.getparent().remove(r._r)
    run = dp.add_run(spec["dates"])
    run.font.name = FONT
    run.font.size = Pt(10)

    proto = main.rows[3]._tr
    for extra in main.rows[3:]:
        extra._tr.getparent().remove(extra._tr)

    for rd in spec["rows"]:
        tr = copy.deepcopy(proto)
        _strip_ids(tr)
        trpr = tr.find(qn("w:trPr"))
        if trpr is not None and trpr.find(qn("w:cantSplit")) is None:
            trpr.insert(0, OxmlElement("w:cantSplit"))   # don't break a task row across pages
        main._tbl.append(tr)
        row = main.rows[-1]
        c_task, c_did, c_time, c_learn = row.cells
        for c in row.cells:
            _clear_cell(c)

        p = c_task.add_paragraph()
        _set_spacing(p, before=4, after=2)
        _add_rich_text(p, rd["task"], size=9.5, base_bold=True)
        if rd.get("task_note"):
            p = c_task.add_paragraph()
            _set_spacing(p, before=0, after=2)
            _add_rich_text(p, rd["task_note"], size=8.5, italic=True)

        for item in rd["did"]:
            p = c_did.add_paragraph()
            _make_bullet(p)
            _set_spacing(p, before=0, after=3)
            _add_rich_text(p, item, size=9)

        p = c_time.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _set_spacing(p, before=4, after=2)
        _style_run(p.add_run(rd["time"]), bold=True, size=9.5)

        p = c_learn.add_paragraph()
        _set_spacing(p, before=4, after=1)
        _style_run(p.add_run("Learning:"), bold=True, size=9.5)
        for item in rd["learning"]:
            p = c_learn.add_paragraph()
            _make_bullet(p)
            _set_spacing(p, before=0, after=2)
            _add_rich_text(p, item, size=8.5)
        p = c_learn.add_paragraph()
        _set_spacing(p, before=4, after=1)
        _style_run(p.add_run("Problems:"), bold=True, size=9.5)
        for item in rd["problems"] or ["None really for this one."]:
            p = c_learn.add_paragraph()
            _make_bullet(p)
            _set_spacing(p, before=0, after=2)
            _add_rich_text(p, item, size=8.5)

    if spec.get("total_time"):
        tr = copy.deepcopy(proto)
        _strip_ids(tr)
        main._tbl.append(tr)
        row = main.rows[-1]
        merged = row.cells[0].merge(row.cells[1])   # merge before clearing
        for c in (merged, row.cells[2], row.cells[3]):
            _clear_cell(c)
            _shade(c, HEADER_FILL)
        p = merged.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        _set_spacing(p, before=3, after=3)
        _style_run(p.add_run("TOTAL TIME THIS WEEK"), bold=True, size=9.5)
        p = row.cells[2].add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _set_spacing(p, before=3, after=3)
        _style_run(p.add_run(spec["total_time"]), bold=True, size=9.5)
        p = row.cells[3].add_paragraph()
        _set_spacing(p, before=3, after=3)
        _style_run(p.add_run(spec.get("total_note", "")), italic=True,
                   size=8.5)
        # keep the header shading for the last cell only
        for tr_el in [row._tr]:
            trpr = tr_el.find(qn("w:trPr"))
            if trpr is not None:
                for h in trpr.findall(qn("w:trHeight")):
                    trpr.remove(h)

    # ---- 4. screenshots / figures section ------------------------------------
    shots_p = None
    for p in doc.paragraphs:
        if p.text.strip().startswith("Screenshots"):
            shots_p = p
            break
    assert shots_p is not None, "template changed: no 'Screenshots:' line"

    # drop the empty filler paragraphs that come after "Screenshots:"
    nxt = shots_p._p.getnext()
    while nxt is not None and nxt.tag == qn("w:p"):
        following = nxt.getnext()
        if not "".join(t.text or "" for t in nxt.iter(qn("w:t"))).strip():
            nxt.getparent().remove(nxt)
        nxt = following

    anchor = shots_p._p
    if spec.get("screenshots_intro"):
        p = _new_paragraph_after(anchor, doc._body)
        _set_spacing(p, before=2, after=6)
        _add_rich_text(p, spec["screenshots_intro"], size=9, italic=True)
        anchor = p._p

    fig_no = 0
    for fig in spec.get("figures", []):
        fig_no += 1
        p = _new_paragraph_after(anchor, doc._body)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _set_spacing(p, before=6, after=2)
        p.paragraph_format.keep_with_next = True   # keep the caption on the same page
        p.add_run().add_picture(fig["path"], width=Inches(fig.get("width", 6.0)))
        cap = _new_paragraph_after(p._p, doc._body)
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _set_spacing(cap, before=0, after=8)
        _add_rich_text(cap, f"Figure {spec['week']}.{fig_no} – {fig['caption']}",
                       size=8.5, italic=True)
        anchor = cap._p

    for ss in spec.get("screenshots", []):
        t = _new_table_after(doc, anchor, rows=1, cols=1)
        _table_borders(t, val="dashed", colour="BF8F00", sz=8)
        _table_width(t, 8965, [8965])
        cell = t.rows[0].cells[0]
        _shade(cell, PLACEHOLDER_FILL)
        _clear_cell(cell)
        p = cell.add_paragraph()
        _set_spacing(p, before=4, after=2)
        _style_run(p.add_run(f"[SCREENSHOT {ss['id']}]  "), bold=True,
                   size=9.5, colour=RGBColor(0x9C, 0x57, 0x00))
        _style_run(p.add_run(ss["title"]), bold=True, size=9.5)
        p = cell.add_paragraph()
        _set_spacing(p, before=0, after=2)
        _add_rich_text(p, "What to capture: " + ss["what"], size=8.5)
        p = cell.add_paragraph()
        _set_spacing(p, before=0, after=4)
        _add_rich_text(p, f"Save as `{ss['file']}` then run "
                          "`python _tools/insert_screenshots.py` "
                          "(or just paste the image here and delete this box).",
                       size=8, italic=True)
        for cp_ in cell.paragraphs:                 # keep box + caption together
            cp_.paragraph_format.keep_with_next = True
        cap = _new_paragraph_after(t._tbl, doc._body)
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _set_spacing(cap, before=2, after=8)
        _add_rich_text(cap, f"Screenshot {ss['id']} – {ss['title']}",
                       size=8.5, italic=True)
        anchor = cap._p

    for note in spec.get("notes", []):
        p = _new_paragraph_after(anchor, doc._body)
        _set_spacing(p, before=4, after=4)
        _add_rich_text(p, note, size=9)
        anchor = p._p

    # ---- 5. tidy-ups ---------------------------------------------------------
    # (a) only keep one blank line between the checklist and the week table
    el = progress_p._p.getnext()
    blanks = []
    while el is not None and el.tag == qn("w:p"):
        blanks.append(el)
        el = el.getnext()
    for extra in blanks[1:]:
        extra.getparent().remove(extra)
    # (b) the template's page-2+ footer says "COS40005_worklog" (copied from
    #     another unit) - make it match the first-page footer
    #     (the text sits inside a content control, so patch the raw w:t nodes)
    for sec in doc.sections:
        t_nodes = list(sec.footer._element.iter(qn("w:t")))
        if "COS40005_worklog" in "".join(t.text or "" for t in t_nodes):
            for t in t_nodes:
                if t.text == "COS4000":
                    t.text = "COS30018_Lab Worklog"
                elif t.text in ("5_", "worklog"):
                    t.text = ""

    # ---- 6. document properties ---------------------------------------------
    cp = doc.core_properties
    cp.title = f"COS30018 Lab Work Log - Week {spec['week']}"
    cp.last_modified_by = spec.get("student_name") or cp.last_modified_by
    cp.modified = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    cp.revision = (cp.revision or 0) + 1

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    doc.save(out_path)
    return out_path
