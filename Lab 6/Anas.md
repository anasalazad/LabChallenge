# Lab 6 (Week 6) – what's left for you, Anas

**Topic:** Naïve Bayes · Principal Component Analysis (PCA)
**Worklog:** `Lab 6/Lab6_Worklog_Week6.docx` (already filled in – 9/12 checklist items done)
**Time you still need:** about 30 min + the two StatQuest videos (~35 min if you watch them)

---

## ✅ Already done for you

| What | File |
|---|---|
| Provided Naïve Bayes notebook – run, outputs saved | `Naive_Bayes.ipynb` |
| Provided PCA notebook – run, with 2 seed lines added (cell 1) so the results are always the same | `PCA.ipynb` |
| Spam example by hand + sklearn check, zero-probability/smoothing, weather example by hand, GaussianNB vs CategoricalNB, wine dataset | `naive_bayes_extras.ipynb` |
| PCA toy example (line search = SVD), PCA by hand with SVD, iris, digits | `pca_extras.ipynb` |
| Plots for the worklog | `figures/6_*.png` |
| The worklog itself | `Lab6_Worklog_Week6.docx` |

## ⬜ What you need to do

Everything in this lab runs **offline**, so you can use Colab **or** Jupyter/VS Code on your laptop (whatever you set up in Lab 5).

### Step 1 – re-run the two provided notebooks (≈10 min) → screenshots 6.1–6.5
**Colab:** File → Upload notebook → `Lab 6/Naive_Bayes.ipynb` → Runtime → Run all. Same for `PCA.ipynb`.
**Laptop:** in the repo folder run `jupyter notebook`, open `Lab 6/Naive_Bayes.ipynb` → Kernel/Run → **Restart & Run All**. Same for `PCA.ipynb`.

Then take:
- 📸 **6.1** `Naive_Bayes.ipynb` → section **"Encoding Features"**: the `le.fit_transform(...)` cells and their printed outputs (`weather: [2 2 0 1 …]`, `Temp: …`, `Play: …`) + the combined `features` list.
- 📸 **6.2** `Naive_Bayes.ipynb` → section **"Generating Model"**: the `GaussianNB()` / `model.fit(features,label)` / `model.predict([[0,2]])` cell with **`Predicted Value: [1]`**.
- 📸 **6.3** `PCA.ipynb` → first cell (imports – **include the 2 seed lines at the bottom**: `rd.seed(42)` / `np.random.seed(42)`), the `data.head()` table and `(100, 10)`.
- 📸 **6.4** `PCA.ipynb` → the **Scree Plot** and **My PCA Graph** (zoom out so both fit, or do two shots named `6.4a_…` and `6.4b_…` – both get inserted).
- 📸 **6.5** `PCA.ipynb` → last code cell (loading scores) + its output (10 students with values ≈ ±0.116).

> With the seed, your PCA numbers should match the worklog exactly (PC1 = 72.9%). If you run the notebook in a different environment and get different numbers, tell Claude locally to update the worklog with yours.

### Step 2 – my extras notebook (≈5 min) → screenshot 6.6
Open `Lab 6/naive_bayes_extras.ipynb` (Colab or laptop), **Run all**, then:
- 📸 **6.6** parts **A and B**: the probability table, `score(N) = … = 0.0923`, `score(S) = … = 0.0136`, `prediction: NORMAL` and the sklearn line `P(class | 'Dear Friend'): {'normal': 0.871, 'spam': 0.129}`.

### Step 3 – the two videos (optional but they're in the lab sheets)
- Naïve Bayes: <https://www.youtube.com/watch?v=O2L2Uv9pdDA>
- PCA: <https://www.youtube.com/watch?v=FgakZw6K1QQ>

(The worklog lists these as "to do" – tick them once watched, or delete that checklist row if you skip them.)

### Step 4 – screenshots into the worklog + final touches
1. Save screenshots in **`Lab 6/screenshots/`** using the names below.
2. `python _tools/insert_screenshots.py 6`
3. Tick the checklist: click the boxes in Word or `python _tools/tick_checklist.py 6 10 11 12`
4. In Word: **Student ID**, check the **dates** (17–23 Sep 2026 – copied from the template), adjust **TIME SPENT** to your real times.

---

## 📸 Screenshot list (Lab 6)

| # | Notebook | Exactly what to capture | Save as |
|---|---|---|---|
| 6.1 | `Naive_Bayes.ipynb` – "Encoding Features" | `le.fit_transform` cells + printed weather/Temp/Play arrays + features list | `screenshots/6.1_nb_encoding.png` |
| 6.2 | `Naive_Bayes.ipynb` – "Generating Model" | GaussianNB fit/predict cell + `Predicted Value: [1]` | `screenshots/6.2_nb_prediction.png` |
| 6.3 | `PCA.ipynb` – top | import cell incl. the 2 seed lines, `data.head()` table, `(100, 10)` | `screenshots/6.3_pca_data.png` |
| 6.4 | `PCA.ipynb` – "Visualise the result" | Scree Plot + My PCA Graph (can be 6.4a + 6.4b) | `screenshots/6.4_pca_plots.png` |
| 6.5 | `PCA.ipynb` – bottom | loading-scores cell + output | `screenshots/6.5_pca_loading_scores.png` |
| 6.6 | `naive_bayes_extras.ipynb` – parts A + B | probability table, score(N)/score(S), sklearn 0.871 | `screenshots/6.6_spam_by_hand.png` |

---

## 🧠 Know your stuff (2-minute revision)
- **Bayes:** `P(c|x) = P(x|c)·P(c) / P(x)`. Naïve Bayes compares `P(c) × Π P(word|c)` for each class and picks the biggest (P(x) is the same for every class so it's skipped).
- **Spam example:** score(Normal) = 8/12 × 8/17 × 5/17 ≈ 0.09 > score(Spam) = 4/12 × 2/7 × 1/7 ≈ 0.01 → "Dear Friend" is normal.
- **Why "naïve":** it assumes features are independent given the class (word order ignored).
- **Zero-frequency problem:** a word never seen in a class makes the whole product 0 → **Laplace smoothing** (add α=1 to all counts).
- **GaussianNB vs CategoricalNB vs MultinomialNB:** continuous features / categories / word counts.
- **PCA:** centre (and scale) the data → PC1 = direction with the most spread (max sum of squared projected distances) → PC2 perpendicular … Explained variance tells you how much info each PC keeps (scree plot). Loading scores = how much each original feature contributes to a PC.
- In `PCA.ipynb`, PC1 = 72.9% → a 2D plot is a good summary; maths and physics scores split into 2 clusters.

> Heads-up: a lot of this was prepared with an AI assistant. Make sure you can explain it in your own words, and check your unit's rules on AI use (add an acknowledgement if they ask for one).
