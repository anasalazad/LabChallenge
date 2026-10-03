# Lab 8 (Week 8) – what's left for you, Anas

**Topic:** RNN · LSTM/GRU · Attention (+ positional encoding)
**Deliverable (hand this in):** the notebook **`Lab8_RNN_LSTM_Attention.ipynb`** + the one-page summary **`Lab8_Summary.pdf`**
**Worklog:** `Lab 8/Lab8_Worklog_Week8.docx` (9/13 checklist items done)
**Time you still need:** about 30 min (or ~45 min if you re-run the notebook yourself)

---

## ✅ Already done for you

| What | File |
|---|---|
| The whole lab: setup, Part 1 (vanishing gradients), Part 2 (RNN/LSTM/GRU × T=5,10,20,60 × 3 seeds + the 128-unit experiment), Part 3 (attention, attention plot, ablation), results table, answers to the 3 checkpoint questions, plus my extra 40-epoch experiment. All code is the lab sheet's – my additions are marked `# (my addition)` | `Lab8_RNN_LSTM_Attention.ipynb` |
| **One-page summary** (results table, gradient plot, attention plot, the 3 answers) – checked it's exactly 1 page | `Lab8_Summary.docx` + `Lab8_Summary.pdf` |
| The script that builds the summary from the notebook's results (re-run it if you re-run the notebook) | `make_summary.py` |
| Raw results | `results.json`, `results_table.csv` |
| Plots | `figures/8_1_gradient_plot.png`, `figures/8_2_attention_plot.png`, `figures/8_3_accuracy_vs_T.png` |
| The worklog | `Lab8_Worklog_Week8.docx` |

My results matched the lab sheet's "typical results" almost exactly (e.g. gradient ratio RNN 1.5e+13, attention 1.00 for every T, ablation 0.26 / 0.18).

## ⬜ What you need to do

### Step 1 – put your student ID on the summary (≈3 min)
Easiest: open `Lab8_Summary.docx` in Word, replace `________` after *Student ID:* with your ID, then **File → Save As → PDF** and overwrite `Lab8_Summary.pdf`.
(Or set `STUDENT_ID = "1234567"` at the top of `make_summary.py`, run `python make_summary.py` in the `Lab 8` folder, then save the .docx as PDF.)

### Step 2 – open the notebook on your laptop (≈5 min, or ~15 min if you re-run)
`jupyter notebook` (or VS Code) → open `Lab 8/Lab8_RNN_LSTM_Attention.ipynb`. The outputs are already saved, so you can screenshot straight away.

*Want your own run?* (nice to have, not required) **Kernel → Restart & Run All** – it takes ~9 min on a laptop CPU (Part 2 alone ~3.5 min, it prints "took …s"). Colab works too (Runtime → Run all, no GPU needed). If you re-run:
1. `python make_summary.py` (in the `Lab 8` folder) to rebuild the summary with your numbers, and re-export the PDF.
2. If any numbers changed, ask Claude locally to update the worklog (it's in `CLAUDE.md`).

### Step 3 – screenshots (≈10 min) → 8.1–8.5
- 📸 **8.1** – setup output (3 rows of 10 digits + `tensor([4, 1, 6])`) **and** the Part 1 cell: the 3 lines `RNN … 1.5e+13`, `LSTM … 7.8e+10`, `GRU … 2.8e+10` + the gradient plot.
- 📸 **8.2** – Part 2: the 12 lines `rnn T= 5 …` to `gru T= 60 …` + `took …s`, and the 3 lines of the 128-unit experiment.
- 📸 **8.3** – Part 3: the 3 `attn` lines (all 1.00) + the attention plot (Head 0 / Head 1).
- 📸 **8.4** – the 2 `attn_nopos` lines (0.26 / 0.18) + the results table.
- 📸 **8.5** – `Lab8_Summary.pdf` open on screen (whole page, with your ID on it).

### Step 4 – hand in
The **notebook** (`Lab8_RNN_LSTM_Attention.ipynb`) and the **one-page summary** (`Lab8_Summary.pdf`) – however your tutor wants it (Canvas upload / email / repo link).

### Step 5 – worklog
1. Screenshots into `Lab 8/screenshots/` → `python _tools/insert_screenshots.py 8`
2. Tick: click the boxes in Word or `python _tools/tick_checklist.py 8 10 11 12 13`
3. **Student ID**, check **dates** (1–7 Oct 2026), adjust **TIME SPENT**.

---

## 📸 Screenshot list (Lab 8)

| # | Where in `Lab8_RNN_LSTM_Attention.ipynb` | Exactly what to capture | Save as |
|---|---|---|---|
| 8.1 | "3. Setup" + "4. Part 1" | 3 rows of digits + labels; 3 gradient-ratio lines + gradient plot | `screenshots/8.1_setup_and_part1.png` |
| 8.2 | "5. Part 2" | 12 result lines + "took …s"; 3 lines of the 128-unit experiment | `screenshots/8.2_part2_results.png` |
| 8.3 | "6. Part 3" | 3 `attn` lines + attention plot (both heads) | `screenshots/8.3_part3_attention.png` |
| 8.4 | "Ablation" + "Results table" | 2 `attn_nopos` lines + the table | `screenshots/8.4_ablation_and_table.png` |
| 8.5 | `Lab8_Summary.pdf` | the whole page with your student ID | `screenshots/8.5_summary_pdf.png` |

---

## 🧠 Know your stuff (2-minute revision – your tutor might ask about the answers)
- **The task:** T random digits, label = the **first** digit → the model must remember step 1 until the end. Chance = 0.10.
- **RNN:** reads one step at a time, hidden state = memory, overwritten every step. **Vanishing gradient:** the training signal shrinks at every step backwards, so the first step gets almost nothing (ratio 1.5×10¹³ for the RNN in Part 1).
- **LSTM/GRU:** add gates (learned switches: write / keep / forget) + a cell state → gradients shrink less (~10¹⁰–10¹¹) → they last longer (GRU perfect at T=10, LSTM 0.47 at T=20) but still fail at T=60.
- **Q2 – different seeds, different results:** the dependency is so hard to find that it's luck whether a run finds it → training on long sequences is unstable, always use several seeds.
- **Attention:** every step looks at every other step directly (1 hop), in parallel → 1.00 even at T=60; the last position puts 0.95/0.80 of its attention on position 0. Cost grows with T².
- **Positional encoding (Q3):** attention by itself is order-blind (a bag of digits). Without position tags the best it can do is guess the most common digit → ≈0.27 at T=10, ≈0.20 at T=30 (what it got: 0.26/0.18). Sin/cos encoding gives each position a unique tag → Transformers/LLMs need it.
- **My extra:** with 40 epochs instead of 15, LSTM/GRU do learn T=20 (0.93/0.96) → partly a training problem, not only memory.

> Heads-up: a lot of this was prepared with an AI assistant. Make sure you can explain every answer in your own words before you hand it in, and check your unit's rules on AI use (add an acknowledgement if they ask for one).
