"""
(Re)builds the weekly worklogs  "Lab N/LabN_Worklog_WeekN.docx"  from the
content files in _tools/worklog_content/weekN.py and the official template.

    python _tools/build_worklogs.py            # weeks 1-4 (5-9 are finished - give the number to rebuild one)
    python _tools/build_worklogs.py 1 3        # just weeks 1 and 3
    python _tools/build_worklogs.py 5 --force  # overwrite even if edited by hand

Safety: every build stores a fingerprint of the generated file in
_tools/.generated_hashes.json. If the .docx was changed afterwards (you edited
it in Word, pasted screenshots, ticked boxes...) the build REFUSES to overwrite
it unless you pass --force, so you can't lose your edits by accident.
"""

import hashlib
import importlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from worklog_builder import REPO_ROOT, build_worklog  # noqa: E402

WEEKS = [1, 2, 3, 4]
HASH_FILE = os.path.join(REPO_ROOT, "_tools", ".generated_hashes.json")


def _sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def out_path(week):
    return os.path.join(REPO_ROOT, f"Lab {week}", f"Lab{week}_Worklog_Week{week}.docx")


def main(argv):
    force = "--force" in argv
    weeks = [int(a) for a in argv if a.isdigit()] or WEEKS
    hashes = {}
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE) as f:
            hashes = json.load(f)

    for week in weeks:
        try:
            mod = importlib.import_module(f"worklog_content.week{week}")
        except ModuleNotFoundError:
            print(f"week {week}: no content file yet (_tools/worklog_content/week{week}.py) - skipped")
            continue
        out = out_path(week)
        rel = os.path.relpath(out, REPO_ROOT)
        if os.path.exists(out) and not force:
            recorded = hashes.get(rel)
            if recorded is None or recorded != _sha(out):
                print(f"week {week}: {rel} has been edited since it was generated "
                      "-> NOT overwriting (use --force if you really want to)")
                continue

        spec = mod.build_spec() if hasattr(mod, "build_spec") else dict(mod.SPEC)
        figures = []
        for fig in spec.get("figures", []):
            fig = dict(fig)
            fig["path"] = os.path.join(REPO_ROOT, fig["path"])
            if not os.path.exists(fig["path"]):
                if fig.get("optional"):
                    print(f"week {week}: optional figure missing, skipped: {fig['path']}")
                    continue
                raise FileNotFoundError(fig["path"])
            figures.append(fig)
        spec["figures"] = figures

        build_worklog(spec, out)
        hashes[rel] = _sha(out)
        print(f"week {week}: wrote {rel}")

    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=2, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
