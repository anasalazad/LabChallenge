"""
Builds my Lab 8 deliverable: the ONE-PAGE summary (results table, gradient plot,
attention plot, answers to the 3 checkpoint questions).

    python make_summary.py            (run inside the "Lab 8" folder)

It reads results.json + figures/ written by Lab8_RNN_LSTM_Attention.ipynb, so if
the notebook is re-run, just run this again. Output: Lab8_Summary.docx
(then File > Save As > PDF in Word, or: soffice --headless --convert-to pdf Lab8_Summary.docx)
"""
import json
import os

import numpy as np
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
STUDENT = "Anas Al Azad"
STUDENT_ID = ""          # <- your student ID

# ---- my answers to the checkpoint questions (2-3 sentences each) -------------
ANSWERS = [
    ("1. In Part 1, which input step has the smallest gradient? What does this mean for learning "
     "the first digit?",
     "{Q1}"),
    ("2. In Part 2, runs with the same settings give different accuracy. What does this tell you "
     "about training RNNs on long sequences?",
     "{Q2}"),
    ("3. In Part 3, accuracy drops when you remove positional encoding. Why?",
     "{Q3}"),
]

ROWS = [("rnn", "RNN"), ("lstm", "LSTM"), ("gru", "GRU"),
        ("rnn-128", "RNN, 128 units"), ("lstm-128", "LSTM, 128 units"), ("gru-128", "GRU, 128 units"),
        ("attn", "Self-attention"), ("attn_nopos", "Attention, no pos. enc.")]
TS = [5, 10, 20, 30, 60]


def load():
    with open(os.path.join(HERE, "results.json")) as f:
        data = json.load(f)
    res = {}
    for key, accs in data["results"].items():
        name, T = key.split("|")
        res[(name, int(T))] = accs
    return data, res


def fmt_answers(data, res):
    """The answers quote my actual numbers, so they're filled in from results.json."""
    g = data["grad_ratio"]
    m = lambda k, T: np.mean(res[(k, T)])
    spread = lambda k, T: (min(res[(k, T)]), max(res[(k, T)]))
    lo, hi = spread("lstm", 20)
    vals = dict(
        Q1=(f"Step 0 (the first input) has by far the smallest gradient for all three layers – the "
            f"last-step/first-step ratio was {g['RNN']:.1e} for the RNN, {g['LSTM']:.1e} for the LSTM and "
            f"{g['GRU']:.1e} for the GRU. The signal from the loss shrinks at every step on the way back, "
            f"so the weights get almost no information about the first digit – exactly the one the "
            f"label depends on. That's why the plain RNN drops to chance (≈0.10) once T gets long."),
        Q2=(f"With identical settings only the random seed (initial weights + data order) changes, yet "
            f"e.g. the LSTM at T = 20 ranged from {lo:.2f} to {hi:.2f}. On long sequences the gradient "
            f"from step 1 is tiny, so whether a run ever “finds” the dependency depends on luck "
            f"in the initialisation – training is unstable, so you need several seeds (and look at "
            f"the spread, not one number) before concluding anything."),
        Q3=(f"Attention is permutation-invariant: it compares every step with every other step by "
            f"content only, so without positional encoding the model can't tell which digit came "
            f"first – the sequence is just a bag of digits. Accuracy fell to "
            f"{m('attn_nopos', 10):.2f} (T = 10) and {m('attn_nopos', 30):.2f} (T = 30) compared with "
            f"{m('attn', 10):.2f} with it; what's left is roughly guessing from digit frequencies. "
            f"The sin/cos encoding gives each position a unique tag, so the last position can attend "
            f"straight to position 0 (weight ≈ {max(data['attention_weight_pos0']):.2f} in my plot)."),
    )
    return [(q, a.format(**vals)) for q, a in ANSWERS]


def shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), fill)
    tcpr.append(shd)


def run(p, text, size=9, bold=False, italic=False, colour=None):
    r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic; r.font.name = "Arial"
    r._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Arial")
    if colour:
        r.font.color.rgb = colour
    return r


def para(doc, before=0, after=2, align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.0
    if align:
        p.alignment = align
    return p


def build():
    data, res = load()
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.top_margin = sec.bottom_margin = Cm(1.3)
    sec.left_margin = sec.right_margin = Cm(1.6)
    doc.styles["Normal"].font.name = "Arial"
    doc.styles["Normal"].font.size = Pt(9)

    p = para(doc, after=0)
    run(p, "COS30018 Intelligent Systems – Lab 8: RNN, LSTM and Attention", 13, bold=True)
    p = para(doc, after=6)
    run(p, f"One-page summary · {STUDENT} · Student ID: ", 9, colour=RGBColor(0x40, 0x40, 0x40))
    run(p, STUDENT_ID or "________", 9, bold=bool(STUDENT_ID))
    run(p, " · Notebook: Lab8_RNN_LSTM_Attention.ipynb", 9, colour=RGBColor(0x40, 0x40, 0x40))

    # ---- results table ---------------------------------------------------------
    p = para(doc, before=2, after=2)
    run(p, "Results (Parts 2 and 3)", 10.5, bold=True)
    run(p, "  – mean test accuracy over 3 seeds; task = recall the first of T random digits; "
           "chance = 0.10", 8.5, italic=True)
    table = doc.add_table(rows=1 + len(ROWS), cols=1 + len(TS))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    for c, text in zip(hdr, ["Model"] + [f"T = {T}" for T in TS]):
        shade(c, "DEEAF6")
        cp = c.paragraphs[0]; cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run(cp, text, 8.5, bold=True)
    for r, (key, label) in zip(table.rows[1:], ROWS):
        cp = r.cells[0].paragraphs[0]
        run(cp, label, 8.5, bold=key in ("attn",))
        for c, T in zip(r.cells[1:], TS):
            cp = c.paragraphs[0]; cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if (key, T) in res:
                v = np.mean(res[(key, T)])
                colour = (RGBColor(0x1E, 0x7B, 0x34) if v >= 0.9 else
                          RGBColor(0xB0, 0x1E, 0x1E) if v <= 0.2 else None)
                run(cp, f"{v:.2f}", 8.5, bold=v >= 0.9, colour=colour)
            else:
                run(cp, "–", 8.5, colour=RGBColor(0x99, 0x99, 0x99))
    for row in table.rows:
        row.cells[0].width = Cm(4.6)
        for c in row.cells[1:]:
            c.width = Cm(2.3)
        for c in row.cells:
            for cp in c.paragraphs:
                cp.paragraph_format.space_before = Pt(0.5)
                cp.paragraph_format.space_after = Pt(0.5)
    p = para(doc, before=2, after=4)
    run(p, "Experiment (32 → 128 hidden units, T = 20) and the ablation (no positional encoding) are "
           "the extra rows. Green = ≥ 0.90, red = ≤ 0.20 (about chance).", 7.5, italic=True,
        colour=RGBColor(0x55, 0x55, 0x55))

    # ---- plots -------------------------------------------------------------------
    p = para(doc, before=2, after=2)
    run(p, "Gradient plot (Part 1) and attention plot (Part 3)", 10.5, bold=True)
    pt = doc.add_table(rows=1, cols=2)
    pt.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c, (img, w) in zip(pt.rows[0].cells, [("figures/8_1_gradient_plot.png", 3.05),
                                               ("figures/8_2_attention_plot.png", 4.0)]):
        cp = c.paragraphs[0]; cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.add_run().add_picture(os.path.join(HERE, img), width=Inches(w))
    pt.rows[0].cells[0].width = Inches(3.15)
    pt.rows[0].cells[1].width = Inches(4.1)
    p = para(doc, before=1, after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    g = data["grad_ratio"]
    w0 = data["attention_weight_pos0"]
    run(p, f"Left: gradient size at each of 50 input steps (log scale) – last/first ratio "
           f"RNN {g['RNN']:.1e}, LSTM {g['LSTM']:.1e}, GRU {g['GRU']:.1e}.  Right: attention of the last "
           f"position at T = 20, averaged over 200 sequences – weight on position 0: head 0 = {w0[0]:.2f}, "
           f"head 1 = {w0[1]:.2f}.", 7.5, italic=True, colour=RGBColor(0x55, 0x55, 0x55))

    # ---- answers -------------------------------------------------------------------
    p = para(doc, before=2, after=2)
    run(p, "Checkpoint questions", 10.5, bold=True)
    for q, a in fmt_answers(data, res):
        p = para(doc, before=2, after=0)
        run(p, q, 8.8, bold=True)
        p = para(doc, before=0, after=2)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run(p, a, 8.8)

    out = os.path.join(HERE, "Lab8_Summary.docx")
    doc.save(out)
    print("wrote", out)


if __name__ == "__main__":
    build()
