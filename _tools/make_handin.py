"""
Make the copy of a worklog that you hand in:  "Completed Labs/Lab N Completed.docx"

    python _tools/make_handin.py 3          # week 3
    python _tools/make_handin.py 1 2 3 4    # several weeks
    python _tools/make_handin.py 3 --force  # overwrite an existing hand-in copy

It takes Lab N/LabN_Worklog_WeekN.docx (after you've rebuilt it with your results and inserted
your screenshots) and removes the parts that are only for you: the checklist, the "My checklist
for this week" line, the "Progress: x/y" line and the "yellow boxes" note. Everything else
(header, task table, figures, screenshots, deliverable and answers) stays exactly the same.
Your worklog itself is not changed.

It also warns you if anything is still unfinished: yellow [SCREENSHOT] boxes that have no image
yet, or yellow highlighted text (numbers that only appear after you run the notebook/scripts).
"""

import os
import sys

from docx import Document
from docx.oxml.ns import qn

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "Completed Labs")


def text_of(el):
    return "".join(t.text or "" for t in el.iter(qn("w:t"))).strip()


def make(week, force=False):
    src = os.path.join(REPO_ROOT, f"Lab {week}", f"Lab{week}_Worklog_Week{week}.docx")
    if not os.path.exists(src):
        print(f"week {week}: {os.path.relpath(src, REPO_ROOT)} not found - build it first "
              f"(python _tools/build_worklogs.py {week})")
        return 1
    out = os.path.join(OUT_DIR, f"Lab {week} Completed.docx")
    if os.path.exists(out) and not force:
        print(f"week {week}: {os.path.relpath(out, REPO_ROOT)} already exists - add --force to replace it")
        return 1

    doc = Document(src)
    body = doc.element.body
    removed = []
    for el in list(body.iterchildren()):
        tag = el.tag.split("}")[1]
        txt = text_of(el)
        if tag == "tbl" and txt.startswith(f"LAB {week} CHECKLIST"):
            body.remove(el)
            removed.append("checklist")
        elif tag == "p" and (txt.startswith("My checklist for this week") or txt.startswith("Progress:")
                             or "yellow boxes" in txt.lower()):
            body.remove(el)
            removed.append(txt[:30])

    # what's still unfinished?
    boxes = [text_of(t._tbl)[:40] for t in doc.tables
             if len(t.rows) == 1 and len(t.columns) == 1 and text_of(t._tbl).startswith("[SCREENSHOT")]
    yellow = []
    for r in body.iter(qn("w:r")):
        hl = r.find(f"{qn('w:rPr')}/{qn('w:highlight')}")
        if hl is not None and hl.get(qn("w:val")) == "yellow":
            yellow.append(text_of(r))
    yellow = [y for y in yellow if y]

    os.makedirs(OUT_DIR, exist_ok=True)
    doc.save(out)
    print(f"week {week}: wrote {os.path.relpath(out, REPO_ROOT)} (removed: checklist, notes for me)")
    if boxes:
        print(f"   ! {len(boxes)} screenshot box(es) still have no image: "
              + ", ".join(b.split("]")[0] + "]" for b in boxes))
    if yellow:
        print(f"   ! {len(yellow)} yellow placeholder(s) left, e.g. '{yellow[0][:50]}' - run the notebook/scripts, "
              f"then rebuild the worklog")
    if not boxes and not yellow:
        print("   everything filled in - ready to hand in")
    return 0


def main(argv):
    force = "--force" in argv
    weeks = [int(a) for a in argv if a.isdigit()]
    if not weeks:
        print(__doc__)
        return 1
    return max(make(w, force) for w in weeks)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
