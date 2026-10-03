"""
Builds START_HERE_click_by_click_guide.pdf (repo root): a beginner, click-by-click
guide for Anas to finish Labs 5-9 (Weeks 5-9).

    python _tools/make_beginner_guide.py

Needs: pip install reportlab   (fonts: DejaVu + Liberation, bundled with most Linux;
on Windows/Mac it falls back to Helvetica - symbols like arrows may look plainer).
"""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "START_HERE_click_by_click_guide.pdf")

# ---------------------------------------------------------------- fonts
D, L = "/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/truetype/liberation/"
try:
    pdfmetrics.registerFont(TTFont("Body", D + "DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("Body-B", D + "DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Body-I", L + "LiberationSans-Italic.ttf"))
    pdfmetrics.registerFont(TTFont("Body-BI", L + "LiberationSans-BoldItalic.ttf"))
    pdfmetrics.registerFont(TTFont("Mono", D + "DejaVuSansMono.ttf"))
    pdfmetrics.registerFont(TTFont("Mono-B", D + "DejaVuSansMono-Bold.ttf"))
    addMapping("Body", 0, 0, "Body"); addMapping("Body", 1, 0, "Body-B")
    addMapping("Body", 0, 1, "Body-I"); addMapping("Body", 1, 1, "Body-BI")
    addMapping("Mono", 0, 0, "Mono"); addMapping("Mono", 1, 0, "Mono-B")
    addMapping("Mono", 0, 1, "Mono"); addMapping("Mono", 1, 1, "Mono-B")
    BODY, BOLD, MONO = "Body", "Body-B", "Mono"
except Exception:                                            # pragma: no cover
    BODY, BOLD, MONO = "Helvetica", "Helvetica-Bold", "Courier"

# ---------------------------------------------------------------- colours
NAVY = colors.HexColor("#1F3A5F")
ORANGE = colors.HexColor("#D9731F")
ORANGE_BG = colors.HexColor("#FFF4E6")
BLUE = colors.HexColor("#2F6FB3")
BLUE_BG = colors.HexColor("#EAF2FB")
RED = colors.HexColor("#C0392B")
RED_BG = colors.HexColor("#FDEDEC")
GREEN = colors.HexColor("#2E7D32")
GREEN_BG = colors.HexColor("#EAF5EA")
GREY_BG = colors.HexColor("#F2F2F2")
GREY = colors.HexColor("#666666")
DARK = colors.HexColor("#1E1E1E")

# ---------------------------------------------------------------- styles
S = {
    "body": ParagraphStyle("body", fontName=BODY, fontSize=10, leading=14.2),
    "small": ParagraphStyle("small", fontName=BODY, fontSize=8.6, leading=11.8, textColor=GREY),
    "h1": ParagraphStyle("h1", fontName=BOLD, fontSize=20, leading=25, textColor=NAVY, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName=BOLD, fontSize=13.5, leading=18, textColor=NAVY,
                         spaceBefore=10, spaceAfter=5),
    "h3": ParagraphStyle("h3", fontName=BOLD, fontSize=11, leading=15, textColor=NAVY,
                         spaceBefore=6, spaceAfter=3),
    "cmd": ParagraphStyle("cmd", fontName=MONO, fontSize=9.6, leading=13, textColor=colors.white),
    "cmdlabel": ParagraphStyle("cmdlabel", fontName=BODY, fontSize=7.8, leading=10,
                               textColor=colors.HexColor("#BBBBBB")),
    "badge": ParagraphStyle("badge", fontName=BOLD, fontSize=11, leading=13, textColor=colors.white,
                            alignment=TA_CENTER),
    "band_t": ParagraphStyle("band_t", fontName=BOLD, fontSize=22, leading=27, textColor=colors.white),
    "band_s": ParagraphStyle("band_s", fontName=BODY, fontSize=11, leading=15,
                             textColor=colors.HexColor("#DCE6F2")),
    "cover_t": ParagraphStyle("cover_t", fontName=BOLD, fontSize=27, leading=33, textColor=NAVY),
    "cover_s": ParagraphStyle("cover_s", fontName=BODY, fontSize=13, leading=18, textColor=GREY),
    "cell": ParagraphStyle("cell", fontName=BODY, fontSize=9, leading=12),
    "cellb": ParagraphStyle("cellb", fontName=BOLD, fontSize=9, leading=12, textColor=colors.white),
}
W = A4[0] - 3.6 * cm          # usable width


def P(text, style="body"):
    return Paragraph(text, S[style])


def key(k):
    """Keyboard key, e.g. key('Ctrl')"""
    return f'<font name="{MONO}" backColor="#E2E2E2">&nbsp;{k}&nbsp;</font>'


def menu(*items):
    """Menu path in bold: menu('Runtime', 'Run all') -> Runtime › Run all"""
    return "<b>" + " › ".join(items) + "</b>"


def mono(t):
    return f'<font name="{MONO}" size="9.2">{t}</font>'


def box(flowables, bg, border, left_bar=True, pad=7):
    t = Table([[flowables]], colWidths=[W])
    style = [("BACKGROUND", (0, 0), (-1, -1), bg),
             ("LEFTPADDING", (0, 0), (-1, -1), pad + (3 if left_bar else 0)),
             ("RIGHTPADDING", (0, 0), (-1, -1), pad),
             ("TOPPADDING", (0, 0), (-1, -1), pad - 1),
             ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]
    if left_bar:
        style.append(("LINEBEFORE", (0, 0), (0, -1), 4, border))
    else:
        style.append(("BOX", (0, 0), (-1, -1), 0.8, border))
    t.setStyle(TableStyle(style))
    return t


def tip(text, title="TIP"):
    return [Spacer(1, 4), box([P(f'<font color="#2F6FB3"><b>{title}</b></font>  {text}')], BLUE_BG, BLUE),
            Spacer(1, 4)]


def warn(text, title="WATCH OUT"):
    return [Spacer(1, 4), box([P(f'<font color="#C0392B"><b>{title}</b></font>  {text}')], RED_BG, RED),
            Spacer(1, 4)]


def mac(text):
    return [Spacer(1, 2), box([P(f'<b>On a Mac:</b> {text}', "small")], GREY_BG, colors.HexColor("#AAAAAA")),
            Spacer(1, 3)]


def cmd(*lines, label="TYPE THIS, then press Enter"):
    rows = [[P(label, "cmdlabel")]] + [[P(l.replace(" ", "&nbsp;") if l.startswith("  ") else l, "cmd")]
                                       for l in lines]
    t = Table(rows, colWidths=[W - 1.1 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), DARK),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                           ("TOPPADDING", (0, 0), (-1, 0), 5), ("BOTTOMPADDING", (0, -1), (-1, -1), 6)]))
    return t


def shot(sid, save_as, what):
    inner = [P(f'<font color="#D9731F"><b>📷 SCREENSHOT {sid}</b></font>'.replace("📷 ", "") +
               f'&nbsp;&nbsp;<font size="8.6" color="#666666">save as</font> {mono(save_as)}'),
             Spacer(1, 2), P(what)]
    return [Spacer(1, 3), box(inner, ORANGE_BG, ORANGE), Spacer(1, 3)]


_step_no = [0]


def reset_steps():
    _step_no[0] = 0


def step(text, *extra):
    """A numbered step; `extra` flowables (commands, boxes) go under the text."""
    _step_no[0] += 1
    badge = Table([[P(str(_step_no[0]), "badge")]], colWidths=[0.75 * cm], rowHeights=[0.62 * cm])
    badge.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    right = [P(text)]
    for e in extra:
        if isinstance(e, list):
            right.extend(e)
        else:
            right.extend([Spacer(1, 4), e])
    inner_w = W - 1.1 * cm
    for f in right:                       # full-width boxes must shrink to fit inside the step
        if isinstance(f, Table) and len(f._argW) == 1 and f._argW[0] and f._argW[0] > inner_w:
            f._argW = [inner_w]
    t = Table([[badge, right]], colWidths=[1.1 * cm, W - 1.1 * cm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def band(title, subtitle):
    t = Table([[[P(title, "band_t"), Spacer(1, 2), P(subtitle, "band_s")]]], colWidths=[W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("LEFTPADDING", (0, 0), (-1, -1), 14),
                           ("TOPPADDING", (0, 0), (-1, -1), 12), ("BOTTOMPADDING", (0, 0), (-1, -1), 13)]))
    return t


def table(rows, widths, header=True, font=9):
    data = []
    for r_i, row in enumerate(rows):
        data.append([P(c, "cellb" if (header and r_i == 0) else "cell") for c in row])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    for i in range(1 if header else 0, len(rows)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F7F9FC")))
    t.setStyle(TableStyle(st))
    return t


def plain_english(text):
    return [box([P('<font color="#2E7D32"><b>WHAT THIS WEEK IS ABOUT (in plain English)</b></font>'),
                 Spacer(1, 3), P(text)], GREEN_BG, GREEN), Spacer(1, 6)]


def finish_week(n, tick_items, extra_note=""):
    """The same 'finish the worklog' routine at the end of every week."""
    items = " ".join(str(i) for i in tick_items)
    reset_steps()
    out = [P(f"Finish your Week {n} worklog", "h2")]
    out.append(step("<b>Close Microsoft Word</b> if it's open (the tools can't change a file that Word has "
                    "open)."))
    out.append(step("In <b>Window B</b> make sure you're in the <b>LabChallenge</b> folder (the line should end "
                    "in <b>LabChallenge&gt;</b> – if it ends in <b>Lab " + str(n) + "&gt;</b>, type "
                    + mono("cd ..") + " and press " + key("Enter") + " first). Then put your screenshots in:",
                    cmd(f"python _tools/insert_screenshots.py {n}"),
                    P("It prints <b>inserted:</b> (the screenshots it put in) and <b>still missing:</b>. "
                      "If something is still missing, check that file's name starts with exactly the right "
                      "number and that it's in the right <b>screenshots</b> folder.", "small")))
    out.append(step("Tick the checklist items you've now done:",
                    cmd(f"python _tools/tick_checklist.py {n} {items}"),
                    P(f"It prints the whole checklist with [x] / [ ]. {extra_note}", "small")))
    out.append(step(f"Open <b>Lab {n} › Lab{n}_Worklog_Week{n}.docx</b> in Word (double-click it in File "
                    "Explorer). Then:",
                    P("• Click on <b>[YOUR STUDENT ID]</b> (yellow, top of page 1) → select it → type your "
                      "student ID. To remove the yellow: select your ID → <b>Home</b> tab → click the arrow "
                      "next to the highlighter pen → <b>No Color</b>.<br/>"
                      "• Check the <b>Dates covered</b> row matches your unit's calendar.<br/>"
                      "• In the <b>TIME SPENT</b> column, change my estimates to roughly how long it really "
                      "took you.<br/>"
                      "• Scroll through once: your screenshots should be where the yellow boxes were. "
                      "<b>Read it</b> – it's written as you, so make sure you'd say it that way.<br/>"
                      f"• Press {key('Ctrl')} + {key('S')} to save.")))
    return [KeepTogether(out)]


# ================================================================= CONTENT
story = []

# ------------------------------------------------------------- cover
story += [Spacer(1, 1.2 * cm),
          P("COS30018 Intelligent Systems", "cover_s"),
          Spacer(1, 4),
          P("Finishing Labs 5 – 9:<br/>a click-by-click guide", "cover_t"),
          Spacer(1, 8),
          P("Written for Anas – no experience needed. Follow it from top to bottom.", "cover_s"),
          Spacer(1, 18)]
story.append(box([
    P("<b>How this guide works</b>"), Spacer(1, 4),
    P("Most of the work in each lab is <b>already done</b> and saved in your GitHub repo: the notebooks are "
      "completed and run, the plots are made, and each week's worklog (the Word file for your tutor) is "
      "already filled in. What's left is the part only <b>you</b> can do: run things on <b>your</b> "
      "computer and in <b>your</b> Google Colab, take screenshots as proof, and finish the worklogs."),
    Spacer(1, 6),
    P("Do <b>Part 0 (setup) once</b>, then one week at a time. You don't need to do it all in one go."),
], BLUE_BG, BLUE, left_bar=False, pad=10))
story.append(Spacer(1, 12))
story.append(P("What the symbols mean", "h3"))
story.append(table([
    ["You'll see…", "It means…"],
    [f"{key('Ctrl')} + {key('S')}", "Press these keys together (hold the first, tap the second)."],
    [menu("File", "Upload notebook"), "Click the <b>File</b> menu, then click <b>Upload notebook</b> in the list."],
    ['<font color="white" backColor="#1E1E1E" name="Mono">&nbsp;black box&nbsp;</font>',
     "A command. Type it <b>exactly</b> (or copy-paste it) into the terminal window, then press "
     f"{key('Enter')}."],
    ['<font color="#D9731F"><b>SCREENSHOT 5.1</b></font>',
     "Take a screenshot now and save it with the name shown (Part 0, section 0.6 shows how)."],
    ['<font color="#2F6FB3"><b>TIP</b></font> / <font color="#C0392B"><b>WATCH OUT</b></font>',
     "Helpful extra info / something that commonly goes wrong."],
], [4.2 * cm, W - 4.2 * cm]))
story.append(Spacer(1, 12))
story.append(P("Time you'll need (roughly)", "h3"))
story.append(table([
    ["Part", "What you'll do", "Time"],
    ["0 · Setup", "Install Python, download your files, make the Python environment", "≈ 45 min (once)"],
    ["Week 5", "Google Colab walkthrough, linear regression in Colab, install scikit-learn", "≈ 1 h"],
    ["Week 6", "Run Naïve Bayes + PCA notebooks on your laptop", "≈ 30 min"],
    ["Week 7", "Install TensorFlow + PyTorch, run the handwritten-digit network", "≈ 45 min"],
    ["Week 8", "Screenshots + put your ID on the one-page summary, hand it in", "≈ 30 min"],
    ["Week 9", "Run the reinforcement-learning notebook in Colab and on your laptop", "≈ 40 min"],
    ["Finish", "Final checks and hand-in", "≈ 20 min"],
], [2.4 * cm, W - 5.6 * cm, 3.2 * cm]))
story.append(PageBreak())

# ------------------------------------------------------------- progress tracker
story.append(P("Your progress tracker", "h1"))
story.append(P("Print this page (or keep it open) and tick things off as you go.", "small"))
story.append(Spacer(1, 6))
tracker = [
    ("Part 0", ["Python 3.12 installed", "Lab files downloaded to Documents › LabChallenge",
                "Virtual environment made (.venv)", "I can take and save a screenshot"]),
    ("Week 5", ["Part A: scikit-learn installed (5.5)", "Part B: Colab walkthrough (5.1 – 5.4)",
                "Part C: Linear_Regression in Colab (5.6, 5.7)", "Worklog finished"]),
    ("Week 6", ["Naive_Bayes + PCA run (6.1 – 6.5)", "Extras screenshot (6.6)", "Videos watched (optional)",
                "Worklog finished"]),
    ("Week 7", ["TensorFlow + PyTorch installed (7.1 – 7.3)", "neural_net run (7.4, 7.5)",
                "Extras screenshots (7.6, 7.7)", "Worklog finished"]),
    ("Week 8", ["Notebook screenshots (8.1 – 8.4)", "Student ID on summary + PDF (8.5)",
                "Notebook + summary handed in", "Worklog finished"]),
    ("Week 9", ["Task 1 in Colab (9.1 – 9.4)", "Task 2 on my laptop (9.5, 9.6)", "Worklog finished"]),
    ("Finish", ["All 5 worklogs have my student ID", "All screenshots in, all boxes ticked",
                "Handed in what my tutor asked for"]),
]
rows = [["", "Task", "Done?"]]
for part, tasks in tracker:
    for i, t in enumerate(tasks):
        rows.append([f"<b>{part}</b>" if i == 0 else "", t, "☐"])
tt = table(rows, [2.2 * cm, W - 4.0 * cm, 1.8 * cm])
story.append(tt)
story.append(PageBreak())

# ------------------------------------------------------------- PART 0
story.append(band("Part 0 · One-time setup", "≈ 45 minutes · you only do this once"))
story.append(Spacer(1, 8))
story += tip("This guide is written for <b>Windows</b> (the lab sheets use Windows). Mac differences are in "
             "grey boxes.")

story.append(P("0.1  Install Python 3.12", "h2"))
reset_steps()
story.append(step("Open your web browser and go to <b>python.org/downloads/windows</b>"))
story.append(step("Scroll down the list until you find <b>Python 3.12.10</b>. Under it, click "
                  "<b>Download Windows installer (64-bit)</b>.",
                  tip("Why 3.12 and not the newest? TensorFlow (Week 7) sometimes doesn't work with the very "
                      "newest Python yet. 3.12 works with everything in these labs.")))
story.append(step("Open the file you downloaded (bottom of your browser, or your <b>Downloads</b> folder)."))
story.append(step("<b>Before clicking anything else:</b> tick the box <b>Add python.exe to PATH</b> at the bottom "
                  "of the first window. Then click <b>Install Now</b>.",
                  warn("If you forget to tick <b>Add python.exe to PATH</b>, the commands later won't work. "
                       "Just run the installer again and tick it.")))
story.append(step("When it says <b>Setup was successful</b>: if you see <b>Disable path length limit</b>, click it "
                  "(click <b>Yes</b> if Windows asks). Then click <b>Close</b>.",
                  P("(This avoids a known problem when installing TensorFlow in Week 7.)", "small")))
story += mac("go to <b>python.org/downloads/macos</b>, find <b>Python 3.12.10</b>, download the "
             "<b>macOS 64-bit universal2 installer</b>, open it and click Continue/Agree/Install. "
             "There's no PATH box on a Mac.")

story.append(P("0.2  Download your lab files from GitHub", "h2"))
reset_steps()
story.append(step("Go to this address (type it into your browser's address bar) and sign in to GitHub if asked:",
                  P(mono("github.com/anasalazad/LabChallenge/tree/claude/optimistic-cray-x20tfr")),
                  P("You should see folders called <b>Lab 5</b>, <b>Lab 6</b> … <b>Lab 9</b> and <b>_tools</b>, "
                    "and a file <b>START_HERE_click_by_click_guide.pdf</b> (this guide).", "small")))
story.append(step("Click the green <b>&lt;&gt; Code</b> button (above the file list, on the right) → click "
                  "<b>Download ZIP</b>."))
story.append(step("Open your <b>Downloads</b> folder → <b>right-click</b> the ZIP file "
                  "(<b>LabChallenge-claude-optimistic-cray-x20tfr.zip</b>) → <b>Extract All…</b> → "
                  "<b>Extract</b>."))
story.append(step("A new folder opens. Keep double-clicking into it until you can <b>see</b> the folders "
                  "<b>Lab 5</b>, <b>Lab 6</b> … <b>Lab 9</b> and <b>_tools</b>. The folder you are now <i>inside</i> "
                  "is the one you want – click the <b>↑</b> arrow (left of the address bar) once so you can see it "
                  "as one folder.",
                  P("ZIP files from GitHub often have a folder inside a folder with the same name – that's "
                    "normal.", "small")))
story.append(step("Drag that folder into <b>Documents</b>. Then right-click it → <b>Rename</b> → type "
                  "<b>LabChallenge</b> → " + key("Enter") + "."))
story.append(Spacer(1, 4))
story.append(box([P("<b>What's inside LabChallenge</b> (the important bits)"), Spacer(1, 3),
                  P(mono("LabChallenge<br/>"
                         "├─ START_HERE_click_by_click_guide.pdf &nbsp;← this guide<br/>"
                         "├─ Anas.md, requirements.txt, README.md<br/>"
                         "├─ Lab 5<br/>"
                         "│&nbsp;&nbsp;├─ Lab5_Worklog_Week5.docx &nbsp;&nbsp;← your worklog for the tutor<br/>"
                         "│&nbsp;&nbsp;├─ Anas.md &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                         "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← more detail for this lab<br/>"
                         "│&nbsp;&nbsp;├─ screenshots\\ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                         "&nbsp;&nbsp;&nbsp;← you save your screenshots here<br/>"
                         "│&nbsp;&nbsp;└─ *.ipynb notebooks, figures\\, …<br/>"
                         "├─ Lab 6 … Lab 9 &nbsp;&nbsp;(same idea)<br/>"
                         "└─ _tools &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;← little helper "
                         "programs (don't touch)"))], GREY_BG, colors.HexColor("#999999"), left_bar=False))
story += tip("Already use git? You can instead run "
             + mono("git clone https://github.com/anasalazad/LabChallenge.git") + " then "
             + mono("git checkout claude/optimistic-cray-x20tfr") + " inside it.")

story.append(P("0.3  Open a terminal inside the folder", "h2"))
story.append(P("A <b>terminal</b> is a window where you type commands. You'll do this step often, so learn it "
               "once:"))
reset_steps()
story.append(step("Open <b>File Explorer</b> → <b>Documents</b> → double-click <b>LabChallenge</b> "
                  "(you should see Lab 5 … Lab 9)."))
story.append(step("Click <b>once</b> on the <b>address bar</b> at the top (where it shows "
                  "<i>Documents › LabChallenge</i>). It turns into text and gets highlighted."))
story.append(step("Type " + mono("cmd") + " and press " + key("Enter") + "."))
story.append(step("A black <b>Command Prompt</b> window opens. The last line looks like "
                  + mono("C:\\Users\\you\\Documents\\LabChallenge&gt;") + " – that means it's working in your "
                  "folder. ✓"))
story += mac("open <b>Terminal</b> (Cmd + Space, type Terminal, Enter), type " + mono("cd ") +
             " (with a space after it), drag the LabChallenge folder from Finder into the Terminal window, "
             "press Enter.")

story.append(P("0.4  Make your Python \"environment\" (once)", "h2"))
story.append(P("This makes a private box of Python libraries just for this unit, inside a hidden folder called "
               "<b>.venv</b>. In the black window from 0.3:"))
reset_steps()
story.append(step("Create it (takes ~30 seconds, prints almost nothing):", cmd("py -3.12 -m venv .venv")))
story.append(step("Switch it on:", cmd(".venv\\Scripts\\activate"),
                  P("Now the line starts with <b>(.venv)</b> – that means it's on. ✓", "small")))
story.append(step("Update pip (the installer tool):", cmd("python -m pip install --upgrade pip")))
story += mac("use " + mono("python3.12 -m venv .venv") + " and then " + mono("source .venv/bin/activate"))
story += warn("<b>The golden rule:</b> every time you open a NEW terminal for this unit, do 0.3 and then run "
              + mono(".venv\\Scripts\\activate") + " first. If the line doesn't start with <b>(.venv)</b>, the "
              "commands in this guide won't find the libraries.", "THE GOLDEN RULE")

story.append(P("0.5  Two terminal windows: A and B", "h2"))
story.append(P("From Week 5 on you'll have <b>two</b> black windows open, both made with 0.3 + activate:"))
story.append(table([
    ["Window", "Used for"],
    ["<b>Window A</b>", "Runs <b>Jupyter</b> (the notebook program). Once it's started, leave it alone – "
                        "don't close it and don't type in it."],
    ["<b>Window B</b>", "Everything else: installing libraries, running the little check scripts, and the "
                        "worklog tools."],
], [3 * cm, W - 3 * cm]))

story.append(P("0.6  How to take and save a screenshot", "h2"))
reset_steps()
story.append(step("Press " + key("Win") + " + " + key("Shift") + " + " + key("S") + ". The screen goes grey."))
story.append(step("Drag a rectangle around exactly what the guide asks for (make sure numbers are readable)."))
story.append(step("A small pop-up appears at the bottom-right (\"Snip copied\"). <b>Click it</b> – the Snipping "
                  "Tool opens with your picture."))
story.append(step("Press " + key("Ctrl") + " + " + key("S") + ". In the Save window go to <b>Documents › "
                  "LabChallenge › Lab 5 › screenshots</b> (use the right lab number), type the file name the "
                  "guide gives you (e.g. " + mono("5.1_colab_first_cells") + ") and click <b>Save</b>.",
                  tip("Only the <b>number at the start</b> of the name really matters (5.1, 5.2 …). "
                      "If one picture isn't enough, save two as <b>5.1a_…</b> and <b>5.1b_…</b> – "
                      "both get used.")))
story += mac("press Cmd + Shift + 4 and drag. The picture lands on your Desktop as \"Screenshot …\". Click its "
             "name, rename it (e.g. 5.1_colab_first_cells) and drag it into the right screenshots folder.")

story.append(KeepTogether([P("0.7  Jupyter and Google Colab in 60 seconds", "h2"), table([
    ["", "Jupyter (on your laptop)", "Google Colab (in the browser)"],
    ["Start / open", "Window A: " + mono("jupyter notebook") + " → your browser opens a page showing your "
                     "folders → click <b>Lab 5</b> → click a file ending in <b>.ipynb</b>",
     "Go to <b>colab.research.google.com</b> → sign in → " + menu("File", "Upload notebook") + " → "
     "<b>Browse</b> → pick the .ipynb file"],
    ["Run everything", menu("Kernel", "Restart Kernel and Run All Cells…") + " → click <b>Restart</b>",
     menu("Runtime", "Run all") + " (if it warns \"not authored by Google\", click <b>Run anyway</b>)"],
    ["Run one cell", "click the cell, press " + key("Shift") + " + " + key("Enter"),
     "click the cell, press " + key("Shift") + " + " + key("Enter")],
    ["Is it finished?", "No cell shows <b>[*]</b> any more", "No cell shows a spinning circle any more"],
    ["Line numbers", "click a cell's left edge, press " + key("Shift") + " + " + key("L") + " (or "
                     + menu("View", "Show Line Numbers") + ")",
     menu("Tools", "Settings", "Editor") + " → tick <b>Show line numbers</b> → <b>Save</b>"],
    ["Save", key("Ctrl") + " + " + key("S"), "Not needed for these labs"],
    ["Stop", "Window A: press " + key("Ctrl") + " + " + key("C") + " (twice if asked) when you're done for "
             "the day", "Just close the tab"],
], [2.5 * cm, (W - 2.5 * cm) / 2, (W - 2.5 * cm) / 2])]))
story.append(PageBreak())

# ------------------------------------------------------------- WEEK 5
story.append(band("Week 5 · Lab 5", "Python intro · Google Colab · scikit-learn · Linear Regression   ·   ≈ 1 hour"))
story.append(Spacer(1, 8))
story += plain_english("You practise Python basics, learn Google Colab (a free website that runs Python, even on "
                       "a GPU), and meet your first machine-learning model: <b>linear regression</b>, which "
                       "draws the best straight line through data – e.g. predicting a house's price from its "
                       "size. Training = finding the line with the smallest total error.")
story.append(P("<b>Already done for you:</b> every Python example run (python_basics_practice.ipynb), a notebook "
               "that walks through the whole Colab guide (colab_walkthrough.ipynb), extra experiments, the plots "
               "and the worklog. <b>You do:</b> parts A–C below, then finish the worklog.", "small"))

story.append(P("Part A · Install scikit-learn + Jupyter on your laptop  (≈ 10 min)", "h2"))
reset_steps()
story.append(step("Open <b>Window B</b>: File Explorer → Documents › LabChallenge → address bar → "
                  + mono("cmd") + " → " + key("Enter") + " → then switch the environment on:",
                  cmd(".venv\\Scripts\\activate")))
story.append(step("Install the libraries (takes 2–5 minutes, lots of text scrolls past):",
                  cmd("pip install scikit-learn notebook numpy pandas matplotlib python-docx pillow"),
                  P("Wait until you get your prompt back. The last lines say <b>Successfully installed …</b>",
                    "small")))
story.append(step("Go into the Lab 5 folder and run the check script:",
                  cmd('cd "Lab 5"', "python screenshot_demo_setup_check.py"),
                  P("It prints the versions and ends with <b>All good - ready for the lab!</b>", "small")))
story.append(step("Take the screenshot:",
                  shot("5.5", "Lab 5\\screenshots\\5.5_local_sklearn_setup.png",
                       "The black window showing the last lines of the pip install <b>and</b> the whole output "
                       "of the check script.")))
story.append(step("Go back up to the LabChallenge folder (you'll need to be there later):", cmd("cd ..")))
story.append(step("Now start Jupyter in a <b>second</b> window – <b>Window A</b>: do 0.3 again (address bar → "
                  + mono("cmd") + "), then:",
                  cmd(".venv\\Scripts\\activate", "jupyter notebook"),
                  P("Your browser opens a page called <b>Jupyter</b> showing your folders. Leave Window A "
                    "open.", "small")))
story.append(step("The lab sheet wants you to try sklearn in a new notebook once: on the Jupyter page click "
                  "<b>New</b> (top right) → <b>Notebook</b> → if asked, pick <b>Python 3 (ipykernel)</b>. In the "
                  "empty box type " + mono("import sklearn") + " and press " + key("Shift") + " + "
                  + key("Enter") + ". No error = it works. ✓ Close that tab.",
                  P("(This made a file called Untitled.ipynb in LabChallenge – you can ignore it or delete it.)",
                    "small")))

story.append(P("Part B · Google Colab walkthrough  (≈ 20 min)", "h2"))
reset_steps()
story.append(step("Go to <b>colab.research.google.com</b> and sign in with your Google account (top right)."))
story.append(step(menu("File", "Upload notebook") + " → <b>Browse</b> → Documents › LabChallenge › Lab 5 › "
                  "<b>colab_walkthrough.ipynb</b> → <b>Open</b>."))
story.append(step(menu("Runtime", "Change runtime type") + " → under <b>Hardware accelerator</b> click "
                  "<b>T4 GPU</b>. <b>Don't click Save yet</b> – screenshot first:",
                  shot("5.2", "Lab 5\\screenshots\\5.2_colab_runtime_gpu.png",
                       "The <b>Change runtime type</b> window with <b>T4 GPU</b> selected."),
                  P("Now click <b>Save</b>.", "small")))
story.append(step("Click on the first grey code cell and press " + key("Shift") + " + " + key("Enter")
                  + " (runs it and jumps to the next one). If a warning appears, click <b>Run anyway</b>. "
                  "Run the first two cells.",
                  shot("5.1", "Lab 5\\screenshots\\5.1_colab_first_cells.png",
                       "The <b>whole browser window</b>: the output <b>Hello from Google Colab!</b>, the text "
                       "cell under it, and your Google account picture in the top-right corner.")))
story.append(step("Keep pressing " + key("Shift") + " + " + key("Enter") + " through section 2 (the GPU check "
                  "and " + mono("!nvidia-smi") + ").",
                  shot("5.3", "Lab 5\\screenshots\\5.3_colab_gpu_check.png",
                       "The output <b>'/device:GPU:0'</b> and the nvidia-smi table under it."),
                  P("No GPU today (empty output or an error)? Colab rations GPUs – just screenshot what you got, "
                    "that's fine.", "small")))
story.append(step("Run the two TPU cells (they'll say <b>Not connected</b> – that's correct, you picked a GPU)."))
story.append(step("Run the " + mono("!pip install pandas") + " cell and the " + mono("!git clone") + " cell. "
                  "Then click the <b>folder icon</b> 📁 on the far-left sidebar.".replace("📁 ", ""),
                  shot("5.4", "Lab 5\\screenshots\\5.4_colab_pip_clone_files.png",
                       "The two cells' output <b>and</b> the Files panel on the left showing the "
                       "<b>Testing-and-Debugging-Tools</b> folder.")))
story.append(step("Run the upload cell: click <b>Choose Files</b> and pick any small file (e.g. "
                  "Lab 5 › Lab5.pdf). Run the Google Drive cell: click <b>Connect to Google Drive</b>, choose "
                  "your account, click <b>Continue</b>/<b>Allow</b>. (No screenshot needed.)"))

story.append(P("Part C · Linear regression in Colab  (≈ 10 min)", "h2"))
reset_steps()
story.append(step(menu("File", "Upload notebook") + " → <b>Browse</b> → Lab 5 › <b>Linear_Regression.ipynb</b>."))
story.append(step(menu("Runtime", "Run all") + ". Wait ~30 seconds (it downloads a house-price dataset)."))
story.append(step("Scroll to the heading <b>3 - Train a model</b>.",
                  shot("5.6", "Lab 5\\screenshots\\5.6_linreg_train.png",
                       "The " + mono("lin_reg.fit(...)") + " cell, the " + mono("lin_reg.coef_") + " output "
                       "(8 numbers) and " + mono("lin_reg.intercept_") + " (about <b>-36.94</b>).")))
story.append(step("Scroll to <b>4 - Test a model</b>.",
                  shot("5.7", "Lab 5\\screenshots\\5.7_linreg_test_mse.png",
                       "The prediction for house 5 (<b>2.675…</b>), the true value (<b>2.697</b>) and both "
                       "mean-squared-error cells (<b>0.5243…</b>).")))
story += tip("<b>Optional bonus:</b> in Jupyter open Lab 5 › <b>linear_regression_extras.ipynb</b> → "
             + menu("Kernel", "Restart Kernel and Run All Cells…") + " → " + key("Ctrl") + " + " + key("S")
             + ". Part D at the bottom now works (it needed internet). If you do this, add <b>11</b> to the tick "
             "command below.")

story += finish_week(5, [8, 9, 10, 12],
                     "Did the optional bonus? Use <b>5 8 9 10 11 12</b> instead.")
story.append(PageBreak())

# ------------------------------------------------------------- WEEK 6
story.append(band("Week 6 · Lab 6", "Naïve Bayes · Principal Component Analysis (PCA)   ·   ≈ 30 minutes"))
story.append(Spacer(1, 8))
story += plain_english("<b>Naïve Bayes</b> guesses a class by multiplying probabilities – like a spam filter: "
                       "\"how often does 'money' appear in spam vs normal emails?\". <b>PCA</b> squashes data with "
                       "many columns into 2 numbers so you can plot it, keeping as much of the information as "
                       "possible.")
story.append(P("<b>Already done:</b> both notebooks run (PCA got a random seed so it gives the same result "
               "every time), my extra notebooks, plots, worklog. <b>You do:</b> run the notebooks yourself and "
               "screenshot them. Everything runs on your laptop – no Colab needed.", "small"))
story += tip("Each time you sit down: Window A = address bar → " + mono("cmd") + " → "
             + mono(".venv\\Scripts\\activate") + " → " + mono("jupyter notebook") + ". Window B = the same but "
             "without the last command.", "START OF EVERY SESSION")
reset_steps()
story.append(step("On the Jupyter page click <b>Lab 6</b> → <b>Naive_Bayes.ipynb</b>. Then "
                  + menu("Kernel", "Restart Kernel and Run All Cells…") + " → <b>Restart</b>. It takes a few "
                  "seconds."))
story.append(step("Scroll to <b>Encoding Features</b>.",
                  shot("6.1", "Lab 6\\screenshots\\6.1_nb_encoding.png",
                       "The " + mono("le.fit_transform(...)") + " cells and their printed outputs "
                       "(weather: [2 2 0 1 …], Temp, Play) and the combined features list.")))
story.append(step("Scroll to <b>Generating Model</b>.",
                  shot("6.2", "Lab 6\\screenshots\\6.2_nb_prediction.png",
                       "The " + mono("GaussianNB()") + " / " + mono("model.fit") + " / "
                       + mono("model.predict([[0,2]])") + " cell with <b>Predicted Value: [1]</b>.")))
story.append(step("Go back to the Jupyter tab with the file list → open <b>PCA.ipynb</b> → "
                  + menu("Kernel", "Restart Kernel and Run All Cells…") + " → <b>Restart</b>. Turn on line "
                  "numbers (click the left edge of a cell, press " + key("Shift") + " + " + key("L") + ").",
                  shot("6.3", "Lab 6\\screenshots\\6.3_pca_data.png",
                       "The first cell <b>including lines 9–11</b> (the seed lines), the " + mono("data.head()")
                       + " table and <b>(100, 10)</b>.")))
story.append(step("Scroll down to the two plots.",
                  shot("6.4", "Lab 6\\screenshots\\6.4_pca_plots.png",
                       "The <b>Scree Plot</b> and <b>My PCA Graph</b>. If they don't fit in one picture, save "
                       "two: 6.4a_… and 6.4b_…")))
story.append(step("Scroll to the last code cell.",
                  shot("6.5", "Lab 6\\screenshots\\6.5_pca_loading_scores.png",
                       "The loading-scores cell and its output (10 students with values around ±0.116).")))
story.append(step("Open <b>naive_bayes_extras.ipynb</b> → " + menu("Kernel", "Restart Kernel and Run All Cells…")
                  + " → <b>Restart</b>.",
                  shot("6.6", "Lab 6\\screenshots\\6.6_spam_by_hand.png",
                       "Parts <b>A and B</b>: the probability table, <b>score(N) = 0.0923</b>, "
                       "<b>score(S) = 0.0136</b>, <b>prediction: NORMAL</b> and the sklearn line with "
                       "<b>'normal': 0.871</b>.")))
story.append(step("Optional but recommended (they're in the lab sheets): watch the two short videos – "
                  "<b>youtube.com/watch?v=O2L2Uv9pdDA</b> (Naïve Bayes) and "
                  "<b>youtube.com/watch?v=FgakZw6K1QQ</b> (PCA)."))
story += finish_week(6, [10, 11, 12], "Didn't watch the videos? Use <b>6 10 12</b>.")
story.append(PageBreak())

# ------------------------------------------------------------- WEEK 7
story.append(band("Week 7 · Lab 7", "TensorFlow & PyTorch · neural networks · handwritten digits   ·   ≈ 45 minutes"))
story.append(Spacer(1, 8))
story += plain_english("A <b>neural network</b> is layers of tiny calculators (neurons) whose weights get "
                       "nudged again and again until it gets the answers right. Here it learns to read "
                       "handwritten digits (0–9) from 28×28-pixel pictures – about 94% correct after 5 rounds "
                       "of training. <b>TensorFlow</b> and <b>PyTorch</b> are the two big libraries for "
                       "building them.")
story.append(P("<b>Already done:</b> the provided notebook (it crashed on the current TensorFlow – fixed), "
               "8 experiments, a PyTorch version, plots, worklog. <b>You do:</b> install both libraries on your "
               "laptop, run the notebook, screenshots.", "small"))
story.append(P("Part A · Install TensorFlow and PyTorch  (≈ 20 min, mostly downloading)", "h2"))
reset_steps()
story.append(step("In your browser go to <b>pytorch.org/get-started/locally</b>. In the grid click: "
                  "<b>PyTorch Build</b> = Stable · <b>Your OS</b> = Windows · <b>Package</b> = Pip · "
                  "<b>Language</b> = Python · <b>Compute Platform</b> = <b>CPU</b>.",
                  shot("7.1", "Lab 7\\screenshots\\7.1_pytorch_selector.png",
                       "The selector grid with your choices and the <b>Run this Command</b> line."),
                  P("Then select the command in <b>Run this Command</b> and press " + key("Ctrl") + " + "
                    + key("C") + " to copy it.", "small")))
story.append(step("In <b>Window B</b> (with (.venv) at the start) install TensorFlow – it's big, give it "
                  "5–10 minutes:", cmd("pip install tensorflow")))
story.append(step("Paste the PyTorch command you copied (" + key("Ctrl") + " + " + key("V") + " or right-click) "
                  "and press " + key("Enter") + ". It looks like " + mono("pip3 install torch torchvision")
                  + ".", warn("If an install fails with a message about long file names/paths, see "
                              "<b>Troubleshooting</b> at the end.")))
story.append(step("Show what's installed:",
                  cmd('pip list | findstr /i "tensorflow keras torch"'),
                  shot("7.2", "Lab 7\\screenshots\\7.2_pip_list.png",
                       "The end of the install output and the <b>pip list</b> lines (tensorflow, keras, "
                       "torch…).")))
story += mac("use " + mono('pip list | grep -iE "tensorflow|keras|torch"'))
story.append(step("Run the check script:",
                  cmd('cd "Lab 7"', "python screenshot_demo_install_check.py", "cd .."),
                  shot("7.3", "Lab 7\\screenshots\\7.3_install_check.png",
                       "The whole output down to <b>Both frameworks work - ready for Lab 7!</b>")))
story.append(P("Part B · Run the digit-recognising network  (≈ 15 min)", "h2"))
reset_steps()
story.append(step("Jupyter → <b>Lab 7</b> → <b>neural_net.ipynb</b> → "
                  + menu("Kernel", "Restart Kernel and Run All Cells…") + " → <b>Restart</b>. The first run "
                  "downloads the digit pictures; training takes 1–2 minutes. Turn on line numbers ("
                  + key("Shift") + " + " + key("L") + ")."))
story.append(step("Scroll to <b>Create our Neural Network</b>.",
                  shot("7.4", "Lab 7\\screenshots\\7.4_nn_model_training.png",
                       "The model cell, all 13 lines (<b>line 2</b> = the seed, <b>lines 6–7</b> = the fix for "
                       "the crash) and the training cell with all <b>5 epochs</b> of output.")))
story.append(step("Scroll to <b>Evaluate the accuracy</b> and <b>Do some predictions</b>.",
                  shot("7.5", "Lab 7\\screenshots\\7.5_nn_test_prediction.png",
                       "<b>Test accuracy: 0.93…</b>, the picture of the digit and <b>Predicted label is: 5</b>."),
                  P("Your numbers may differ slightly in the 3rd decimal – that's normal.", "small")))
story.append(step("Open <b>nn_experiments.ipynb</b>. <b>Don't re-run it</b> (it takes ~5 minutes; the results "
                  "are already saved). Scroll to part B.",
                  shot("7.6", "Lab 7\\screenshots\\7.6_experiments_table.png",
                       "The 8 printed experiment lines and the results table under them.")))
story.append(step("Open <b>nn_pytorch.ipynb</b> (no need to re-run).",
                  shot("7.7", "Lab 7\\screenshots\\7.7_pytorch_training.png",
                       "The training cell and its 5 epoch lines (test accuracy ≈ 0.976).")))
story.append(step("Optional (it's in the lab sheet): watch <b>youtube.com/watch?v=aircAruvnKk</b> "
                  "(3Blue1Brown – \"But what is a neural network?\")."))
story += finish_week(7, [8, 9, 10, 11], "Skipped the video? Use <b>7 8 9 11</b>.")
story.append(PageBreak())

# ------------------------------------------------------------- WEEK 8
story.append(band("Week 8 · Lab 8", "RNN · LSTM/GRU · Attention   ·   ≈ 30 minutes   ·   has a hand-in"))
story.append(Spacer(1, 8))
story += plain_english("Some data comes in a <b>sequence</b> (words, stock prices). The test here: the model "
                       "sees a list of random digits and must remember the <b>first</b> one. Older models "
                       "(<b>RNN</b>) forget over long lists, <b>LSTM/GRU</b> remember a bit longer, and "
                       "<b>attention</b> (what ChatGPT-style models use) can look straight back at the first "
                       "digit – but it needs <b>positional encoding</b> to know the order.")
story += warn("This lab has a <b>deliverable</b>: you hand in the notebook "
              "<b>Lab8_RNN_LSTM_Attention.ipynb</b> and the one-page summary <b>Lab8_Summary.pdf</b>. Both are "
              "ready – you only add your student ID.", "HAND-IN")
reset_steps()
story.append(step("Jupyter → <b>Lab 8</b> → <b>Lab8_RNN_LSTM_Attention.ipynb</b>. <b>Don't re-run it</b> – it "
                  "takes about 10 minutes and the results are already saved. Just scroll."))
story.append(step("Top of the notebook:",
                  shot("8.1", "Lab 8\\screenshots\\8.1_setup_and_part1.png",
                       "Setup output (3 rows of 10 digits + " + mono("tensor([4, 1, 6])") + ") and Part 1: the "
                       "3 lines <b>RNN … 1.5e+13 / LSTM … 7.8e+10 / GRU … 2.8e+10</b> and the gradient plot. "
                       "Two pictures (8.1a, 8.1b) is fine.")))
story.append(step("Part 2:",
                  shot("8.2", "Lab 8\\screenshots\\8.2_part2_results.png",
                       "The 12 lines from <b>rnn T= 5</b> to <b>gru T= 60</b>, the <b>took …s</b> line and the 3 "
                       "lines of the 128-unit experiment.")))
story.append(step("Part 3:",
                  shot("8.3", "Lab 8\\screenshots\\8.3_part3_attention.png",
                       "The 3 <b>attn</b> lines (all 1.00) and the attention plot (Head 0 / Head 1).")))
story.append(step("Ablation + results table:",
                  shot("8.4", "Lab 8\\screenshots\\8.4_ablation_and_table.png",
                       "The 2 <b>attn_nopos</b> lines (0.26 / 0.18) and the results table.")))
story.append(step("Open <b>Lab 8 › Lab8_Summary.docx</b> in Word. After <b>Student ID:</b> replace "
                  "<b>________</b> with your ID."))
story.append(step(menu("File", "Save As") + " → <b>Browse</b> → make sure you're in the <b>Lab 8</b> folder → "
                  "<b>Save as type</b>: choose <b>PDF (*.pdf)</b> → file name <b>Lab8_Summary</b> → <b>Save</b> → "
                  "if asked to replace, click <b>Yes</b>. Then close Word.",
                  P("Open the new Lab8_Summary.pdf and check it's still <b>one page</b>.", "small")))
story.append(step("With the PDF open:",
                  shot("8.5", "Lab 8\\screenshots\\8.5_summary_pdf.png",
                       "The whole page of <b>Lab8_Summary.pdf</b> with your student ID visible.")))
story.append(step("<b>Hand in</b> the two files the way your tutor asked (e.g. Canvas upload): "
                  "<b>Lab8_RNN_LSTM_Attention.ipynb</b> and <b>Lab8_Summary.pdf</b>, both in the Lab 8 folder."))
story += finish_week(8, [10, 11, 12, 13], "Not handed in yet? Leave out <b>12</b> and tick it later with "
                     + mono("python _tools/tick_checklist.py 8 12") + ".")
story.append(PageBreak())

# ------------------------------------------------------------- WEEK 9
story.append(band("Week 9 · Lab 9", "Reinforcement learning with Gymnasium (Q-learning)   ·   ≈ 40 minutes"))
story.append(Spacer(1, 8))
story += plain_english("In <b>reinforcement learning</b> an \"agent\" learns by trial and error: it tries an "
                       "action, gets a reward or penalty, and slowly learns which actions pay off. Here a taxi "
                       "learns to pick up and drop off passengers, and a cart learns to balance a pole. "
                       "<b>Task 1</b> = fill in the missing code (done), <b>Task 2</b> = make it run on your own "
                       "laptop (your job).")
story.append(P("Task 1 · In Google Colab  (≈ 15 min)", "h2"))
reset_steps()
story.append(step("Colab → " + menu("File", "Upload notebook") + " → <b>Browse</b> → Lab 9 › "
                  "<b>Lab_Week 9.ipynb</b>."))
story.append(step(menu("Runtime", "Run all") + " → <b>Run anyway</b> if warned. It takes 3–5 minutes (the "
                  "first cell installs things; the cart-pole training is the slow part)."))
story.append(step("Turn on line numbers: " + menu("Tools", "Settings", "Editor") + " → tick <b>Show line "
                  "numbers</b> → <b>Save</b>."))
story.append(step("Find the long cell that starts with " + mono("import math") + " and contains "
                  + mono("class QLearningAgent") + ". It's long, so take <b>three</b> pictures:",
                  shot("9.1a", "Lab 9\\screenshots\\9.1a_qlearning_code.png",
                       "That cell, <b>lines 47 to 103</b> (get_value, update, get_best_action)."),
                  shot("9.1b", "Lab 9\\screenshots\\9.1b_qlearning_code.png",
                       "Same cell, <b>lines 107 to 140</b> (get_action)."),
                  shot("9.1c", "Lab 9\\screenshots\\9.1c_play_and_train.png",
                       "The " + mono("play_and_train") + " cell, <b>lines 10 to 25</b>.")))
story.append(step("Scroll to the taxi training cell (the one with the reward plot).",
                  shot("9.2", "Lab 9\\screenshots\\9.2_taxi_training.png",
                       "The reward plot with <b>no red AssertionError</b> under it, plus the next cell's output "
                       "(mean reward of the last 100 episodes ≈ <b>7.78</b>).")))
story.append(step("Scroll to the <b>Discretizer</b> cell and the CartPole training below it.",
                  shot("9.3", "Lab 9\\screenshots\\9.3_cartpole_training.png",
                       "The Discretizer cell (<b>lines 13–19</b>), the training plot and the <b>How did it go?</b> "
                       "output (ewma ≈ <b>135.9</b>). Split into 9.3a / 9.3b if needed.")))
story.append(step("Scroll to the very end (CliffWalking).",
                  shot("9.4", "Lab 9\\screenshots\\9.4_evsarsa_vs_qlearning.png",
                       "The benchmark plot, the two lines <b>Q-learning … / EV-SARSA …</b> and the picture of "
                       "the two paths.")))
story.append(P("Colab may give slightly different numbers than mine – that's fine as long as there's no "
               "error.", "small"))
story.append(P("Task 2 · On your own laptop  (≈ 20 min)", "h2"))
reset_steps()
story.append(step("In <b>Window B</b> install the RL libraries:",
                  cmd('pip install "gymnasium[classic-control,toy-text]" tqdm')))
story.append(step("Run the check script:",
                  cmd('cd "Lab 9"', "python screenshot_demo_gym_check.py", "cd .."),
                  shot("9.5", "Lab 9\\screenshots\\9.5_local_gym_check.png",
                       "The end of the pip install and the whole output down to <b>Gymnasium works locally - "
                       "ready for Lab 9!</b>")))
story.append(step("Jupyter → <b>Lab 9</b> → <b>Lab_Week 9.ipynb</b> → "
                  + menu("Kernel", "Restart Kernel and Run All Cells…") + " → <b>Restart</b>. Wait 2–5 minutes.",
                  P("The first cell may print <b>'bash' is not recognized…</b> or <b>No such file or "
                    "directory</b> – <b>ignore it</b>, it's a Colab-only trick that isn't needed on a "
                    "laptop.", "small")))
story.append(step("Scroll to the finished taxi training cell.",
                  shot("9.6", "Lab 9\\screenshots\\9.6_local_jupyter_run.png",
                       "The <b>whole browser window</b> so the address bar shows <b>localhost:8888</b> (that "
                       "proves it's running on your laptop, not Colab) and the finished taxi cell.")))
story += finish_week(9, [8, 9, 10, 11])
story.append(PageBreak())

# ------------------------------------------------------------- FINISH
story.append(band("Final checks & hand-in", "≈ 20 minutes"))
story.append(Spacer(1, 8))
reset_steps()
story.append(step("Check everything is in. In Window B (in the LabChallenge folder):",
                  cmd("python _tools/insert_screenshots.py --check"),
                  P("Every lab should say <b>still missing: nothing - all screenshots in!</b>", "small")))
story.append(step("Open each of the 5 worklogs once more and check: your <b>student ID</b> is there, no yellow "
                  "boxes left, all the checklist boxes you've done are ticked (you can also just <b>click</b> a "
                  "box in Word to tick it), times look right."))
story.append(step("If your tutor wants PDFs: in Word " + menu("File", "Save As") + " → <b>Save as type</b> = "
                  "<b>PDF</b> → <b>Save</b>, for each worklog."))
story.append(step("Hand in what your tutor asked for (the 5 worklogs, plus the Lab 8 notebook + summary if not "
                  "done yet)."))
story.append(step("Before anyone asks you questions about it: open <b>Anas.md</b> inside each Lab folder and read "
                  "the <b>Know your stuff</b> section (2 minutes each). It explains each lab in simple words."))
story += warn("A lot of this work was prepared with an AI assistant. Make sure you can explain it in your own "
              "words, and check your unit's rules on using AI – if they ask you to say so, add one line to each "
              "worklog (e.g. under Problems: \"I used an AI assistant to help with …\").", "BE HONEST")

story.append(PageBreak())
story.append(P("Troubleshooting", "h1"))
story.append(table([
    ["What you see", "What to do"],
    ["<b>'python' is not recognized…</b> or <b>'py' is not recognized…</b>",
     "Python isn't on PATH. Run the Python installer again, tick <b>Add python.exe to PATH</b>. Then close "
     "and reopen the black window."],
    ["The line doesn't start with <b>(.venv)</b>", "Run " + mono(".venv\\Scripts\\activate") + " (you must be "
     "in the LabChallenge folder)."],
    ["<b>ModuleNotFoundError: No module named …</b> in a notebook",
     "Jupyter was started without (.venv), or that week's install step was skipped. In Window A press "
     + key("Ctrl") + " + " + key("C") + ", activate, run " + mono("jupyter notebook") + " again, and do the "
     "install step for that week."],
    ["TensorFlow won't install: <b>No matching distribution found</b>",
     "Your environment isn't Python 3.12. Check with " + mono("python --version") + ". If it's wrong, delete "
     "the .venv folder and redo Part 0.4."],
    ["Install fails mentioning a very long path / <b>OSError … No such file or directory</b>",
     "Windows' long-path limit. Run the Python 3.12 installer again → <b>Repair</b> → on the last screen click "
     "<b>Disable path length limit</b>. Then try the install again."],
    ["Jupyter didn't open in the browser",
     "In Window A, find the line starting with <b>http://localhost:8888/…</b>, copy it into your browser."],
    ["A cell shows <b>[*]</b> for a long time", "It's still working – wait. Lab 7 experiments and Lab 8 take "
     "several minutes. To stop it: " + menu("Kernel", "Interrupt Kernel") + "."],
    ["<b>PermissionError</b> when running insert_screenshots / tick_checklist",
     "The worklog is open in Word. Close Word and run it again."],
    ["insert_screenshots says <b>still missing</b> but I saved it",
     "Check the file is in the right <b>Lab N › screenshots</b> folder, the name starts with exactly the right "
     "number (e.g. <b>7.3_</b>), and it's a .png or .jpg."],
    ["<b>No worklogs found</b>", "You're not in the LabChallenge folder. Type " + mono("cd ..") + " and try "
     "again."],
    ["Colab: <b>Cannot connect to GPU backend</b>", "Click <b>Connect without GPU</b> and carry on – screenshot "
     "the message for 5.3, it's fine."],
    ["The Snipping Tool pop-up disappeared", "Open <b>Snipping Tool</b> from the Start menu, or press "
     + key("Win") + " + " + key("Shift") + " + " + key("S") + " again."],
    ["Anything else", "Each Lab folder's <b>Anas.md</b> has more detail. You can also open the LabChallenge folder "
     "in Claude Code and say <i>\"Read CLAUDE.md and help me with Week N\"</i> – or ask your tutor."],
], [6 * cm, W - 6 * cm]))


# ================================================================= build
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont(BODY, 8)
    canvas.setFillColor(GREY)
    if doc.page > 1:
        canvas.drawString(1.8 * cm, A4[1] - 1.2 * cm, "COS30018 Labs 5–9 · click-by-click guide")
        canvas.setStrokeColor(colors.HexColor("#DDDDDD"))
        canvas.line(1.8 * cm, A4[1] - 1.35 * cm, A4[0] - 1.8 * cm, A4[1] - 1.35 * cm)
    canvas.drawRightString(A4[0] - 1.8 * cm, 1.1 * cm, f"page {doc.page}")
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm,
                            topMargin=1.7 * cm, bottomMargin=1.6 * cm,
                            title="COS30018 Labs 5-9 - click-by-click guide",
                            author="Prepared for Anas Al Azad", subject="How to finish Labs 5-9")
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
