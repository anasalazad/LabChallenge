# Lab 8 (Week 8) – instructions for Claude (local session)

Continuing work from a cloud session. Read the repo-root `CLAUDE.md` first. This folder is **Lab 8** (RNN, LSTM/GRU, attention; PyTorch). It has a **graded-style deliverable: the notebook + a ONE-PAGE summary** (results table model×T for Parts 2–3, the gradient plot, the attention plot, answers to the 3 checkpoint questions in 2–3 sentences each).

## Files
| File | Status |
|---|---|
| `Lab_8.pdf` | lab sheet (read-only) |
| `Lab8_RNN_LSTM_Attention.ipynb` | built from the sheet's code **verbatim**; additions marked `# (my addition)` (savefig, `results` dict, results table, `results.json`, Q3 check cell, 40-epoch extra). Executed (~8.5 min on 4 CPU threads). Answers to the checkpoint questions are in the markdown cell under "7. Checkpoint questions". |
| `results.json`, `results_table.csv` | written by the notebook |
| `figures/8_1_gradient_plot.png`, `8_2_attention_plot.png`, `8_3_accuracy_vs_T.png` | written by the notebook |
| `make_summary.py` | builds `Lab8_Summary.docx` from `results.json` + figures (answers are templated with the real numbers) |
| `Lab8_Summary.docx` / `.pdf` | the one-page deliverable (verified 1 page via LibreOffice) |
| `Lab8_Worklog_Week8.docx` | `_tools/build_worklogs.py` ← `_tools/worklog_content/week8.py`; 9/13 checklist items done |

Cloud results (matched the sheet's "typical results"): grad ratio RNN 1.5e13 / LSTM 7.8e10 / GRU 2.8e10; Part 2 means T=5/10/20/60: RNN 1.00/0.66/0.10/0.10, LSTM 1.00/0.96/0.47/0.09, GRU 1.00/1.00/0.10/0.09; 128 units @T=20: 0.77/0.59/1.00; attention 1.00/1.00/1.00; weights on pos 0: 0.95/0.80; no-pos ablation 0.26 (T=10) / 0.18 (T=30); extra 40 epochs @T=20: RNN 0.55, LSTM 0.93, GRU 0.96.

## Remaining work you CAN do
1. **Student ID** (only when Anas gives it): set `STUDENT_ID` in `make_summary.py`, run `python make_summary.py` (from inside `Lab 8`), then convert to PDF: `soffice --headless --convert-to pdf Lab8_Summary.docx` (or ask Anas to Save As PDF in Word). Check it's still **1 page** (`pdfinfo Lab8_Summary.pdf`). Also put the ID in `_tools/worklog_content/week8.py` (`student_id`) and rebuild – or type it in the docx if Anas has edited it.
2. **If Anas re-runs the notebook** (optional, ~9 min CPU): `jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=7200 Lab8_RNN_LSTM_Attention.ipynb`, then `python make_summary.py` + PDF again. If numbers differ from the list above, update `_tools/worklog_content/week8.py` and the notebook's answer markdown cell, then `python _tools/build_worklogs.py 8` (or python-docx edits if the worklog was already edited by Anas – never `--force` over their edits).
3. **Screenshots:** `Lab 8/screenshots/8.1_*` … `8.5_*` → `python _tools/insert_screenshots.py 8`.
4. **Checklist:** items 10–13 are Anas's → `python _tools/tick_checklist.py 8 <n>`.

## Don'ts
- Don't change the lab sheet's model/training code (the summary + worklog quote its results). Additions only, marked `# (my addition)`.
- Don't let the summary spill onto a second page.
- Don't run TensorFlow in the same kernel (see root `CLAUDE.md`).
