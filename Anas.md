# Anas – start here 👋

All five labs (5–9) have been worked through. Every lab folder now has:

- **`LabN_Worklog_WeekN.docx`** – your worklog for that week, built from the tutor's template (same Swinburne header/logo, same table). It starts with a **checklist** (☒ done / ☐ still to do), then the task table (*What I did · Time spent · Learning & Problems*), then the plots, then **yellow boxes where your screenshots go**.
- **`Anas.md`** – step-by-step what *you* still need to do for that lab + the exact screenshots to take (which notebook, which cells, what file name).
- **`CLAUDE.md`** – instructions for Claude Code on your laptop, if you want it to do the remaining technical bits for you.
- **`screenshots/`** – save your screenshots here.

## Where each lab stands

| Lab | Week / dates* | Topic | Done for you | Still for you | Your time |
|---|---|---|---|---|---|
| [Lab 5](Lab%205/Anas.md) | 5 · 10–16 Sep | Python, Google Colab, sklearn, Linear Regression | 7/12 | Colab walkthrough, run LinReg in Colab, local sklearn install, screenshots | ~1 h |
| [Lab 6](Lab%206/Anas.md) | 6 · 17–23 Sep | Naïve Bayes, PCA | 9/12 | re-run 2 notebooks + screenshots, 2 videos (optional) | ~30 min |
| [Lab 7](Lab%207/Anas.md) | 7 · 24–30 Sep | TensorFlow & PyTorch, neural nets, MNIST | 7/11 | install TF + PyTorch on your laptop, run MNIST notebook, screenshots | ~45 min |
| [Lab 8](Lab%208/Anas.md) | 8 · 1–7 Oct | RNN / LSTM / GRU / Attention + **deliverable** (notebook + one-page summary – both ready) | 9/13 | student ID on the summary, screenshots, hand in notebook + summary | ~30 min |
| [Lab 9](Lab%209/Anas.md) | 9 · 8–14 Oct | Reinforcement learning (Gymnasium, Q-learning) – Task 1 notebook completed | 7/11 | Task 1 in Colab + Task 2 on your laptop, screenshots | ~40 min |

\*Dates are worked out from the template (Week 6 = 17–23 Sep 2026). If your unit had a mid-semester break, fix them in each worklog.

## One-time setup (≈15 min, do this first)

1. **Python 3.10–3.12** installed (`python --version`). TensorFlow can lag behind the newest Python, so 3.11/3.12 is the safe pick.
2. **Google account** for Colab (Labs 5–9 can all run in Colab).
3. Open a terminal in the repo folder and make a virtual environment with everything:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate            # Windows   (Mac/Linux: source .venv/bin/activate)
   pip install -r requirements.txt   # numpy, sklearn, jupyter, tensorflow, torch, gymnasium, python-docx...
   ```
   Then `jupyter notebook` opens Jupyter in your browser (or open the .ipynb files in VS Code).

> ⚠️ The Lab 7 and Lab 9 guides ask you to screenshot the *install* itself (pip / pytorch.org) – so if you want those screenshots to look natural, do the installs as described there instead of all at once here. Either way works.

## The screenshot workflow (same for every lab)
1. Follow `Lab N/Anas.md` → take each 📸 screenshot (Windows: `Win + Shift + S`, Mac: `Cmd + Shift + 4`).
2. Save it into `Lab N/screenshots/` with the name it gives (e.g. `5.3_colab_gpu_check.png` – only the `5.3` part has to be exact; a shot split in two can be `5.3a_…` + `5.3b_…`).
3. Drop them all into the worklogs in one go:
   ```bash
   python _tools/insert_screenshots.py           # all labs   (or: ... 5 7  for just labs 5 and 7)
   python _tools/insert_screenshots.py --check   # just list what's still missing
   ```
   (Or paste them into Word by hand and delete the yellow boxes.)
4. Tick the checklist items you finished – click the boxes in Word, or:
   ```bash
   python _tools/tick_checklist.py 5             # shows lab 5's items with numbers
   python _tools/tick_checklist.py 5 8 9 10      # ticks items 8, 9, 10
   ```

## Before you hand anything in ✅
- [ ] **Student ID** typed into all 5 worklogs (yellow box at the top) + the Lab 8 summary.
- [ ] Dates right for your unit's calendar.
- [ ] **TIME SPENT** column = your real times (mine are estimates).
- [ ] All yellow screenshot boxes replaced, all checklist boxes you've done ticked.
- [ ] Read each worklog once – it's written in your voice, so make sure you'd say it that way.
- [ ] **Lab 8 deliverable:** `Lab 8/Lab8_RNN_LSTM_Attention.ipynb` + `Lab 8/Lab8_Summary.pdf` (one page).
- [ ] If your tutor wants PDFs: in Word *File → Save As → PDF* for each worklog.

## Getting this onto your laptop
Everything is on GitHub on the branch `claude/optimistic-cray-x20tfr`. In your clone:
```bash
git fetch origin
git checkout claude/optimistic-cray-x20tfr
```
When you're happy with it, open a pull request from that branch into `main` on GitHub (or merge locally: `git checkout main && git merge claude/optimistic-cray-x20tfr && git push`).

## Using Claude Code on your laptop for the rest
Open the repo folder in Claude Code and say e.g. *"Read CLAUDE.md and Lab 5/CLAUDE.md and finish what's left for Lab 5"*. It knows how to run the blocked bits, update the worklogs, insert screenshots and tick boxes. It can't log into Colab or take screenshots of your screen – that part's you.

## Things that didn't work in the cloud (so you know)
- **California Housing download** (Lab 5) – the cloud network blocked `ndownloader.figshare.com`. Works in Colab / on your laptop; `Lab 5/CLAUDE.md` has the steps.
## Two honest notes
- Bugs found in the tutor's material (worth mentioning in class): Lab 7's notebook crashes on current TensorFlow (`InputLayer(input_shape=28*28)` → fixed with `shape=(28*28,)`); Lab 6's PCA notebook isn't reproducible (no random seed – added one); the template's page-2 footer said "COS40005_worklog" (fixed in the generated worklogs).
- A lot of this was prepared with an AI assistant. Go through each lab's **"Know your stuff"** section so you can explain the work yourself, and check your unit's rules on AI use – if they ask for an acknowledgement, add one to your worklogs.
