# Week 6 worklog content - Lab 6 (Naive Bayes + PCA)
# Markup: **bold**, `code`. Edit text here, then: python _tools/build_worklogs.py 6

SPEC = {
    "week": 6,
    "dates": "17-23 September 2026",
    "student_name": "Anas Al Azad",
    "student_id": "",
    "title": "Week 6 – Naïve Bayes & Principal Component Analysis (PCA)",
    "intro": "My checklist for this week – ticked = done (all notebooks + plots are in the **Lab 6** "
             "folder of my repo), unticked = still on my to-do list.",
    "checklist": [
        ("Read the Week 6 tutorial (Naïve Bayes) and the PCA PDF", True),
        ("Spam example by hand: “Dear Friend” → 0.09 vs 0.01 = normal, and checked it with "
         "sklearn `MultinomialNB` (`naive_bayes_extras.ipynb`)", True),
        ("Zero-probability problem + Laplace smoothing (“Lunch Money Money Money Money”)", True),
        ("Ran `Naive_Bayes.ipynb` (Overcast + Mild → play) and checked the answer by hand", True),
        ("Compared `GaussianNB` vs `CategoricalNB` on all 9 weather/temp combos", True),
        ("Extra: Naïve Bayes on a real dataset (wine) with train/test split + confusion matrix", True),
        ("Ran `PCA.ipynb` (added a random seed so it's reproducible): scree plot, PCA graph, loading scores", True),
        ("Extra: PCA toy example (line search = SVD) + PCA by hand with numpy SVD = sklearn "
         "(`pca_extras.ipynb`)", True),
        ("Extra: PCA on iris (4D → 2D) and handwritten digits (64D → 2D)", True),
        ("Re-run `Naive_Bayes.ipynb` + `PCA.ipynb` myself and take screenshots 6.1–6.6", False),
        ("Watch the two StatQuest videos linked in the sheets (Naïve Bayes + PCA)", False),
        ("Add my screenshots (yellow boxes below)", False),
    ],
    "rows": [
        {
            "task": "Naïve Bayes theory – spam example",
            "task_note": "Week 6 tutorial sheet",
            "did": [
                "Redid the sheet's example in Python with exact fractions: p(Dear|N) = 8/17 = 0.47 … "
                "p(Money|S) = 4/7 = 0.57. **score(N) = 0.092 vs score(S) = 0.014 → normal**, same "
                "as the sheet. Normalising gives P(normal | Dear Friend) = 0.87.",
                "Made up 12 emails whose word counts add up to the sheet's table and trained sklearn's "
                "`MultinomialNB` on them – exactly the same probabilities (0.871).",
                "Tried “Lunch Money Money Money Money”: without smoothing it's classed as "
                "**normal** because p(Lunch|Spam) = 0 wipes out the spam score. With Laplace "
                "smoothing (α = 1) it's correctly **spam** (Fig 6.1).",
            ],
            "time": "1.5 h",
            "learning": [
                "Posterior ∝ prior × likelihoods; you can skip p(x) when comparing classes.",
                "“Naïve” = assumes features are independent (word order doesn't matter at all).",
                "One zero count kills the whole product → always smooth (that's sklearn's `alpha`).",
            ],
            "problems": [
                "sklearn needs one row per email, not word totals, so I had to invent emails that "
                "match the totals.",
                "sklearn won't take α = 0 exactly (clips it to 1e-10 with a warning), so I used "
                "`alpha=1e-10, force_alpha=True` for the “no smoothing” version.",
            ],
        },
        {
            "task": "Naïve Bayes notebook",
            "task_note": "`Naive_Bayes.ipynb`",
            "did": [
                "Ran it: `LabelEncoder` turns the strings into numbers (Overcast=0, Rainy=1, Sunny=2 / "
                "Cool=0, Hot=1, Mild=2 / No=0, Yes=1), zipped weather + temp into features, trained "
                "`GaussianNB` → **Predicted Value: [1]** (play) for Overcast + Mild.",
                "Checked it by hand from the counts: score(Yes) = 9/14 × 4/9 × 4/9 = 0.127, "
                "score(No) = 5/14 × 0/5 × 2/5 = 0 → Yes ✔.",
                "Compared `GaussianNB` with `CategoricalNB` on all 9 weather × temp combos – "
                "they agree on 8, but **not on Sunny + Cool** (Gaussian: No, Categorical: Yes 0.55).",
            ],
            "time": "1 h",
            "learning": [
                "LabelEncoder numbers categories alphabetically.",
                "GaussianNB assumes each feature is a continuous bell curve, so it treats the 0/1/2 "
                "codes like real numbers – CategoricalNB is the right one for categories.",
            ],
            "problems": [
                "My printed features list looks different from the tutor's: `[[np.int64(2), "
                "np.int64(1)], …]` instead of `[[2, 1], …]`. It's just how NumPy 2 prints "
                "numbers now – same values.",
            ],
        },
        {
            "task": "PCA theory + toy example",
            "task_note": "PCA PDF, `pca_extras.ipynb` part A",
            "did": [
                "Read the PCA PDF (centre the data, best-fit line through the origin = PC1, PC2 "
                "perpendicular, eigenvector/eigenvalue, loading scores, variation = SS/(n−1), "
                "scree plot).",
                "Made my own 6-sample, 2-gene example and found PC1 the PDF's way: tried every line "
                "through the origin and kept the one with the biggest **SS(distances)** → 19.5°, "
                "unit vector [0.943, 0.334]. numpy SVD gives [0.942, 0.336] – same line (Fig 6.5).",
                "PC1 = 96.3% of the variation, PC2 = 3.7%.",
            ],
            "time": "1.5 h",
            "learning": [
                "PCA really is “the direction where the projected points are most spread out”.",
                "“Minimise the distance to the line” = “maximise the projected distance "
                "from the origin” – Pythagoras, because each point's distance from the origin "
                "is fixed.",
                "Eigenvalue = SS of the projected distances; variation = eigenvalue / (n−1).",
            ],
            "problems": [
                "The PDF's example values are only in the pictures, so I couldn't copy its exact data "
                "– made my own 6 points instead (so my slope isn't the PDF's 1/4).",
            ],
        },
        {
            "task": "PCA notebook",
            "task_note": "`PCA.ipynb` + `pca_extras.ipynb` part B",
            "did": [
                "Ran it: 100 students × 10 random scores (5 maths, 5 physics), scaled, `PCA()` "
                "fit/transform, scree plot and PCA graph.",
                "Added `rd.seed(42)` and `np.random.seed(42)` so I get the same data every run.",
                "Results: **PC1 = 72.9%** of the variance (PC2 only 5.6%) (Fig 6.3); the maths and "
                "physics scores form two separate clusters along PC1 (Fig 6.4); top loading scores "
                "are all ≈ ±0.116 so lots of students contribute equally.",
                "Did the same PCA by hand (centre + `np.linalg.svd`) – identical explained "
                "variance to sklearn.",
            ],
            "time": "1 h",
            "learning": [
                "sklearn's PCA = centring + SVD, nothing magic.",
                "Scaling first matters, otherwise big-number features dominate.",
            ],
            "problems": [
                "The original notebook has no seed, so every run gives different data/plots.",
                "The notebook text says physics is on the **left**, mine is on the **right** – PCs "
                "only have a direction up to a sign, so plots can come out mirrored.",
                "Comment says “we create 6 maths scores” but `range(1,6)` gives 5 (stop is "
                "exclusive) – that's why the shape is (100, 10) not (100, 12).",
            ],
        },
        {
            "task": "Extra – real datasets",
            "task_note": "`naive_bayes_extras.ipynb` E, `pca_extras.ipynb` C–D",
            "did": [
                "`GaussianNB` on sklearn's wine data (178 wines, 13 features, 3 classes), 70/30 "
                "split: **54/54 test wines correct**, 96.8% on the training set (Fig 6.2).",
                "PCA on iris (4 features): PC1 + PC2 = 95.8% of the variance and setosa separates "
                "completely along PC1; loadings show PC1 ≈ petal length/width + sepal length (Fig 6.6).",
                "PCA on 8×8 digits (64 features): 2 PCs keep only 28.5% and need 29 PCs for 95%, "
                "so the 2D plot overlaps a lot.",
            ],
            "time": "1.5 h",
            "learning": [
                "NB is super fast and surprisingly good on clean continuous data.",
                "Whether a 2D PCA plot is useful depends on the scree plot (iris yes, digits not really).",
            ],
            "problems": [
                "The wine test set is small (54), so 100% is partly luck – a different split would "
                "probably miss one or two.",
            ],
        },
    ],
    "total_time": "6.5 h",
    "total_note": "+ ~30 min to re-run & screenshot, + the 2 videos",
    "screenshots_intro": "Figures 6.1–6.6 are straight out of my notebooks (6.3 and 6.4 are from the "
                         "provided `PCA.ipynb`, the rest from my extras notebooks). The yellow boxes are "
                         "screenshots I still need to add.",
    "figures": [
        {"path": "Lab 6/figures/6_1_spam_smoothing.png", "width": 4.8,
         "caption": "“Lunch Money Money Money Money” – without smoothing the spam score is 0, "
                    "with Laplace smoothing it's correctly spam"},
        {"path": "Lab 6/figures/6_2_wine_confusion_matrix.png", "width": 3.0,
         "caption": "GaussianNB on the wine test set (54 wines) – confusion matrix"},
        {"path": "Lab 6/figures/6_3_pca_scree_plot.png", "width": 3.6,
         "caption": "scree plot from PCA.ipynb – PC1 explains 72.9% of the variance"},
        {"path": "Lab 6/figures/6_4_pca_graph.png", "width": 3.9,
         "caption": "PCA graph from PCA.ipynb – maths and physics scores form two clusters along PC1"},
        {"path": "Lab 6/figures/6_5_pca_toy_line_search.png", "width": 5.6,
         "caption": "my toy example: PC1 found by trying every line through the origin (max SS) matches SVD"},
        {"path": "Lab 6/figures/6_6_iris_pca.png", "width": 5.6,
         "caption": "PCA on iris – scree plot and the 150 flowers in PC1/PC2 space"},
    ],
    "screenshots": [
        {"id": "6.1", "title": "Naive_Bayes.ipynb – encoding the features",
         "what": "the “Encoding Features” cells: the `le.fit_transform(...)` code and the printed "
                 "weather / Temp / Play arrays + the combined features list.",
         "file": "Lab 6/screenshots/6.1_nb_encoding.png"},
        {"id": "6.2", "title": "Naive_Bayes.ipynb – training + prediction",
         "what": "the “Generating Model” cell (`GaussianNB()`, `model.fit(...)`, "
                 "`model.predict([[0,2]])`) with the output **Predicted Value: [1]**.",
         "file": "Lab 6/screenshots/6.2_nb_prediction.png"},
        {"id": "6.3", "title": "PCA.ipynb – the generated student data",
         "what": "the import cell (with my 2 seed lines at the bottom), `data.head()` table and the "
                 "`(100, 10)` shape output.",
         "file": "Lab 6/screenshots/6.3_pca_data.png"},
        {"id": "6.4", "title": "PCA.ipynb – scree plot + PCA graph",
         "what": "both plots with the code cells above them (zoom out a bit so both fit, or take two "
                 "screenshots 6.4a / 6.4b).",
         "file": "Lab 6/screenshots/6.4_pca_plots.png"},
        {"id": "6.5", "title": "PCA.ipynb – loading scores",
         "what": "the last code cell and its output (top 10 students and their PC1 loading scores).",
         "file": "Lab 6/screenshots/6.5_pca_loading_scores.png"},
        {"id": "6.6", "title": "naive_bayes_extras.ipynb – spam example by hand vs sklearn",
         "what": "parts A and B: the probability table, score(N) = 0.0923 vs score(S) = 0.0136 and "
                 "the sklearn output P(class | 'Dear Friend') = 0.871.",
         "file": "Lab 6/screenshots/6.6_spam_by_hand.png"},
    ],
}
