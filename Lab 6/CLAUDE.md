# Lab 6 (Week 6) – instructions for Claude (local session)

Continuing work from a cloud session. Read the repo-root `CLAUDE.md` first. This folder is **Lab 6 = Week 6 tutorial**: Naïve Bayes (sklearn) + PCA (sklearn). Everything here runs offline – nothing was blocked in the cloud, so this lab is essentially complete apart from things only Anas can do.

## Files
| File | Origin | Status |
|---|---|---|
| `Lab_6.pdf`, `Principal component analysis (PCA).pdf` | tutor | lab sheets (read-only) |
| `Naive_Bayes.ipynb`, `naive_bayes.py` | tutor | notebook executed in the cloud (code unchanged) |
| `PCA.ipynb` | tutor | executed; **only change:** 2 seed lines appended to the import cell (`rd.seed(42)`, `np.random.seed(42)`) for reproducibility. Results: PC1 72.9%, PC2 5.6% |
| `naive_bayes_extras.ipynb`, `pca_extras.ipynb` | cloud session | executed, outputs + figures saved |
| `figures/6_1…6_7*.png` | generated | 6_1–6_6 embedded in the worklog (6_7 digits only in the notebook) |
| `Lab6_Worklog_Week6.docx` | `_tools/build_worklogs.py` ← `_tools/worklog_content/week6.py` | 9/12 checklist items done |
| `screenshots/` | – | Anas puts `6.1_*.png` … `6.6_*.png` here |

## Remaining work you CAN help with
1. *(Optional)* re-execute the notebooks in Anas's local environment to confirm they run there:
   ```bash
   cd "Lab 6"
   for nb in Naive_Bayes.ipynb PCA.ipynb naive_bayes_extras.ipynb pca_extras.ipynb; do
     jupyter nbconvert --to notebook --execute --inplace "$nb"; done
   ```
   With the seeds the numbers should be identical (PC1 72.9%, wine test 54/54, iris PC1+PC2 95.8%). If any number differs (different library versions), update `_tools/worklog_content/week6.py` and rebuild (`python _tools/build_worklogs.py 6`), or – if the docx was already edited by Anas (the build script will refuse) – edit the docx in place with python-docx. Never use `--force` on a worklog Anas has edited.
2. **Screenshots:** check `Lab 6/screenshots/` names (6.1–6.6; 6.4 may be split into `6.4a_…` + `6.4b_…` – the insert tool handles that and inserts both in order). Then `python _tools/insert_screenshots.py 6`.
3. **Checklist:** items 10–12 are Anas's (re-run + screenshots, StatQuest videos, add screenshots). Tick with `python _tools/tick_checklist.py 6 <n>` once Anas confirms.

## Only Anas can do
Watching the videos, taking screenshots, student ID, confirming dates/time spent.

## Conventions
Worklog text = Anas's informal first-person student voice; only claim things that actually happened. Don't edit the tutor's PDFs; don't commit `*.bak.docx`.
