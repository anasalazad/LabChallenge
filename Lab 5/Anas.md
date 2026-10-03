# Lab 5 (Week 5) – what's left for you, Anas

**Topic:** Python intro · Google Colab · scikit-learn · Linear Regression
**Worklog:** `Lab 5/Lab5_Worklog_Week5.docx` (already filled in – 7/12 checklist items done)
**Time you still need:** about 45–60 min (mostly Colab + screenshots)

---

## ✅ Already done for you

| What | File |
|---|---|
| Every Python example from the lab sheet, run, plus a "my try" cell after each topic | `python_basics_practice.ipynb` |
| A notebook that walks through the whole Colab PDF (GPU check, pip, git clone, upload, Drive) – ready to upload to Colab | `colab_walkthrough.ipynb` |
| Extra experiments: 3-house example, gradient descent from scratch, learning-rate test, train/test split | `linear_regression_extras.ipynb` |
| Plots for the worklog | `figures/5_1…5_3*.png` |
| One-screen setup check for your laptop (for screenshot 5.5) | `screenshot_demo_setup_check.py` |
| The worklog itself (checklist, task table, learning/problems, figures, screenshot boxes) | `Lab5_Worklog_Week5.docx` |

## ⬜ What you need to do

### Step 1 – Google Colab (≈20 min) → screenshots 5.1–5.4
1. Go to <https://colab.research.google.com> and sign in with your Google account.
2. **File → Upload notebook** → pick `Lab 5/colab_walkthrough.ipynb` from this repo.
3. **Runtime → Change runtime type → Hardware accelerator: T4 GPU**.
   📸 **5.2** – take the screenshot *while this dialog is open* (T4 GPU selected), then press **Save**.
4. Run the first two cells (click ▶ or **Shift+Enter**).
   📸 **5.1** – whole browser window: the "Hello from Google Colab!" output + the text cell under it + your account icon top-right.
5. Run the GPU cells (`tf.test.gpu_device_name()` and `!nvidia-smi`).
   📸 **5.3** – both outputs: `'/device:GPU:0'` and the nvidia-smi table.
   *(If it says no GPU: Colab gave you none today – try again later or just screenshot what you get, it's still evidence.)*
6. Run the TPU checks (they'll just say "Not connected" on a GPU runtime – that's fine).
7. Run `!pip install pandas` and the `!git clone ...` cell. Click the 📁 **Files** icon on the left.
   📸 **5.4** – the two cells' output + the Files pane showing the `Testing-and-Debugging-Tools` folder.
8. Run the upload cell (pick any small file) and the Drive cell (click *Connect to Google Drive* and allow). Optional screenshot – not required.

### Step 2 – Linear_Regression.ipynb in Colab (≈10 min) → screenshots 5.6, 5.7
1. Colab → **File → Upload notebook** → `Lab 5/Linear_Regression.ipynb`.
2. **Runtime → Run all**. (The dataset downloads by itself – takes a few seconds.)
3. 📸 **5.6** – scroll to **"3 - Train a model"**: the `lin_reg.fit(...)` cell, the `lin_reg.coef_` output (8 numbers) and `lin_reg.intercept_` (−36.94…).
4. 📸 **5.7** – **"4 - Test a model"**: `predict(...)` → `2.675…`, `data.target[5]` → `2.697`, and both MSE cells → `0.5243…`.
5. *(Optional but nice)* upload `linear_regression_extras.ipynb` too and **Run all** – part D at the bottom (California Housing train/test split) only works with internet, which Colab has. Then download it (**File → Download → .ipynb**) and replace the one in the repo, and save the last plot as `Lab 5/figures/5_4_california_pred_vs_true.png` – or just ask Claude locally to do this part (it's in `CLAUDE.md`).

### Step 3 – scikit-learn on your laptop (≈10 min) → screenshot 5.5
Open a terminal (Git Bash / PowerShell / Terminal on Mac) **in the repo folder**:
```bash
pip install scikit-learn notebook        # (if you use the repo venv: see the main Anas.md)
cd "Lab 5"
python screenshot_demo_setup_check.py
```
📸 **5.5** – the terminal with the pip command (or at least its last lines) and the whole output of the script, down to *"All good - ready for the lab!"*.

The lab sheet also says: run `jupyter notebook`, click **New → Python 3**, type `import sklearn` and run it. Do that once so you've seen it (no screenshot needed unless you want an extra one).

### Step 4 – put the screenshots in the worklog (≈5 min)
1. Save each screenshot into **`Lab 5/screenshots/`** with the name from the table below (only the number at the start really matters, e.g. `5.3_anything.png` works).
2. From the repo root run:
   ```bash
   python _tools/insert_screenshots.py 5
   ```
   Every yellow box that has a matching image gets swapped for the image. (Or paste them into Word yourself and delete the yellow boxes.)
3. Tick the checklist: click the boxes in Word, or run
   `python _tools/tick_checklist.py 5 8 9 10 12` (add `11` if you did step 2.5).

### Step 5 – final touches in Word
- [ ] Type your **Student ID** (yellow box at the top).
- [ ] Check the **dates** (I used 10–16 September 2026, worked backwards from the template's Week 6 = 17–23 Sep). Fix it if your unit had a break in between.
- [ ] Check the **TIME SPENT** numbers – they're my estimates, change them to what it actually took you.
- [ ] Read it through once so you know what it says (your tutor might ask).

---

## 📸 Screenshot list (Lab 5)

| # | Where | Exactly what to capture | Save as |
|---|---|---|---|
| 5.1 | Colab – `colab_walkthrough.ipynb` | Whole browser window: first code cell + its output "Hello from Google Colab!", the text cell below, account icon visible | `screenshots/5.1_colab_first_cells.png` |
| 5.2 | Colab – Runtime → Change runtime type | The dialog with **T4 GPU** selected | `screenshots/5.2_colab_runtime_gpu.png` |
| 5.3 | Colab – `colab_walkthrough.ipynb`, section 2 | `tf.test.gpu_device_name()` → `'/device:GPU:0'` + `!nvidia-smi` table | `screenshots/5.3_colab_gpu_check.png` |
| 5.4 | Colab – sections 3–5 | `!pip install pandas` + `!git clone` output, **Files pane open** showing `Testing-and-Debugging-Tools` | `screenshots/5.4_colab_pip_clone_files.png` |
| 5.5 | Your laptop – terminal | `pip install scikit-learn notebook` + full output of `python screenshot_demo_setup_check.py` | `screenshots/5.5_local_sklearn_setup.png` |
| 5.6 | Colab – `Linear_Regression.ipynb`, "3 - Train a model" | `lin_reg.fit(...)`, `lin_reg.coef_` (8 weights), `lin_reg.intercept_` (−36.94) | `screenshots/5.6_linreg_train.png` |
| 5.7 | Colab – `Linear_Regression.ipynb`, "4 - Test a model" | predict sample 5 (2.675), true value (2.697), both MSE cells (0.5243) | `screenshots/5.7_linreg_test_mse.png` |

**Screenshot tips:** Windows `Win + Shift + S` (snip an area) · Mac `Cmd + Shift + 4` · zoom the browser to ~90% if a section doesn't fit · make sure the output numbers are readable.

---

## 🧠 Know your stuff (2-minute revision in case your tutor asks)
- **Linear regression** fits a line/plane `y = w0 + w1·x1 + … + wn·xn` by finding the weights that minimise the cost `J(w) = ½ Σ (ŷ − y)²` (sum of squared errors).
- **Gradient descent** updates `w = w − α·∇J(w)`. Learning rate **α** too small → slow, too big → overshoots/diverges (my Fig 5.2 shows this). Scale your features first.
- sklearn's `LinearRegression` doesn't use α – it solves least squares directly.
- **MSE** = mean of squared errors. The provided notebook measures it on the training data (0.524); a **train/test split** gives a fairer number.
- Python: dynamically typed, `//` floor division, `%` remainder, `range(10)` = 0..9, indentation defines blocks.
- Colab: free GPU/TPU (time-limited), `!` runs shell commands, files in `/content` disappear when the runtime resets → mount Drive.

> Heads-up: a lot of this was prepared with an AI assistant. Make sure you can explain everything in here in your own words, and check your unit's rules on AI use – if they ask you to acknowledge AI help, add a line to your worklog.
