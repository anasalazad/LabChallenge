# Week 10 worklog content - Lab 10 (genetic algorithms with PyGAD: linear model + 8 Queen puzzle)
# Markup: **bold**, `code`, [[yellow = still to fill in]].
# Numbers come from Lab 10/Lab10_Genetic_Algorithms.ipynb (run with PyGAD 3.8.1, fixed seeds), saved in
# Lab 10/results/lab10_results.json.      python _tools/build_worklogs.py 10

TUNING = [
    ["Sheet settings (50 generations, 8 per population)", "0.0073", "0.0331", "14/20"],
    ["200 generations", "0.0013", "0.0133", "19/20"],
    ["50 per population", "0.0016", "0.0079", "20/20"],
    ["200 generations + 50 per population", "**0.0003**", "**0.0012**", "**20/20**"],
    ["Tournament selection", "0.0094", "0.0482", "10/20"],
    ["Roulette wheel selection", "0.0112", "0.0601", "8/20"],
    ["Uniform crossover", "0.0145", "0.0348", "8/20"],
    ["Mutate 50% of genes", "0.0294", "0.0994", "6/20"],
]
QUEENS = [
    ["App settings, original attack count", "14/30 (47%)", "60", "1.3 s"],
    ["App settings, fixed attack count", "20/30 (67%)", "55", "1.2 s"],
    ["Integer genes (my change)", "13/30 (43%)", "71", "1.3 s"],
    ["Permutation – each column once (my change)", "**30/30 (100%)**", "1", "0.1 s"],
]
FIXES = [
    ["`fitting_linear_model.py`", "`fitness_func(solution, solution_idx)` → *ValueError: fitness_func must accept 3 "
     "positional arguments* (PyGAD 3 passes the GA as well).", "`fitness_func(ga_instance, solution, solution_idx)`"],
    ["`fitting_linear_model.py`", "`plot_result()` doesn't exist any more → *AttributeError*.", "`plot_fitness()`"],
    ["`8_queen_puzzle.py`", "Pressing **Initial Population** crashed: *unexpected keyword argument "
     "'delay_after_gen'* (removed in PyGAD 3).", "Removed it; a 0.2 s pause in the generation callback instead, and "
     "`stop_criteria=\"reach_1.1\"` so it stops when the puzzle is solved."],
    ["`8_queen_puzzle.py`", "**Start GA** called `thread.run()`, which runs the GA on the window's own thread, so the "
     "board froze until it finished.", "`thread.start()`, and the board is redrawn with `Clock.schedule_once` (only "
     "the window's thread may draw)."],
    ["`8_queen_puzzle.py`", "`attacks_diagonal` never reset its running total for each queen, so attacks were "
     "over-counted – 126 instead of 28 when all queens are on one diagonal.", "Reset `total = 0` for each queen – "
     "now it counts each attacking pair once."],
]
QA = [
    ("How does a genetic algorithm work?",
     "It keeps a population of possible answers. Each generation it scores them with the fitness function, picks the "
     "best as parents, mixes pairs of parents (crossover) to make children, randomly changes a few genes (mutation), "
     "and repeats. Good answers spread, bad ones die out – like evolution."),
    ("Why is the fitness 1 / |output − 44| and not just the error?",
     "PyGAD always tries to make fitness bigger. The error should get smaller, so flipping it (1 / error) turns 'small "
     "error' into 'big fitness'. For the queens it's the same idea with the number of attacks, and 1.1 when there are "
     "none (because 1/0 would break)."),
    ("Why doesn't the GA always find the best answer?",
     "It's random and only tries a small part of all possible answers. It can get stuck when the population becomes "
     "too similar (my linear run stopped improving after generation 4), and with a bad starting population or too "
     "few generations it runs out of time – the app settings solved the queens only 20 times out of 30."),
    ("What made the biggest difference?",
     "For the linear model: a bigger population and more generations (median error 0.0073 → 0.0003). For the queens: "
     "choosing a better way to write the answer down. Making each answer a permutation removes all column attacks, so "
     "the GA only has to sort out the diagonals – it solved all 30 runs."),
    ("How is this different from the search and learning we did before?",
     "Q-learning (Week 9) learns from rewards step by step, and gradient descent (Week 5) follows the slope of the "
     "error. A GA needs neither – just a way to score a whole answer – so it works even when there's no slope to "
     "follow, like placing queens on a board."),
]


def build_spec():
    return {
        "week": 10,
        "dates": "5–11 October 2026",
        "student_name": "Anas Al Azad",
        "student_id": "105694136",
        "title": "Week 10 – Genetic algorithms with PyGAD (linear model + 8 Queen puzzle)",
        "intro": "My checklist for this week – ticked = done, unticked = still to do. Everything is in the "
                 "`Lab 10` folder of my repo (`Lab10_Genetic_Algorithms.ipynb` + the two fixed tutor programs).",
        "checklist": [
            ("Read the Week 10 sheet (PyGAD, fitting a linear model, 8 Queen puzzle)", True),
            ("Fixed the tutor's two programs so they run with PyGAD 3 (table below)", True),
            ("Linear model with the sheet's settings – output 43.9933 (target 44)", True),
            ("Extra: tuned the GA – 8 settings × 20 seeds", True),
            ("8 Queens: ran the app's GA 30 times without the GUI + found and fixed the attack-count bug", True),
            ("Extra: two better encodings for the queens (integer genes, permutation)", True),
            ("Install PyGAD + Kivy on my laptop", False),
            ("Run `fitting_linear_model.py` on my laptop", False),
            ("Run the 8 Queen app (`8_queen_puzzle.py`) until it finds 0 attacks", False),
            ("Screenshots added (yellow boxes below)", False),
        ],
        "rows": [
            {
                "task": "PyGAD basics",
                "task_note": "Sheet part 1",
                "did": [
                    "Installed PyGAD (version 3.8.1 – the sheet talks about 3.1.0).",
                    "Learned the 4 steps: write a fitness function → choose the parameters → create `pygad.GA` → "
                    "`run()`. Tried the 'fitness = sum of the solution' example on 3 made-up solutions "
                    "(fitness 750, 949 and 263).",
                ],
                "time": "0.5 h",
                "learning": [
                    "A GA works on a population of answers: the fittest become parents, crossover mixes them, "
                    "mutation adds small random changes, repeat each generation.",
                    "The fitness function is the only part that's specific to the problem.",
                ],
                "problems": [
                    "The sheet's code is for an older PyGAD – the fitness function now needs 3 inputs "
                    "(`ga_instance, solution, solution_idx`).",
                ],
            },
            {
                "task": "Fitting a linear model",
                "task_note": "Sheet part 2, `fitting_linear_model.py`",
                "did": [
                    "Found 6 weights so that 4w1 − 2w2 + 3.5w3 + 5w4 − 11w5 − 4.7w6 = 44, with the sheet's "
                    "settings (50 generations, 8 solutions, steady-state selection, single-point crossover).",
                    "Best weights [3.64, 1.65, 4.47, 0.01, −1.37, −0.43] → output **43.9933** (fitness 149). The "
                    "error went from 1.78 to 0.0067 by **generation 4**, then didn't improve for the other 46 "
                    "generations (Fig 10.1).",
                    "Two other seeds gave completely different weights that also give ≈ 44.",
                ],
                "time": "1 h",
                "learning": [
                    "1 equation and 6 unknowns means there are endless right answers – the GA just finds one.",
                    "With only 8 solutions the population quickly becomes all the same, and then it gets stuck.",
                ],
                "problems": [
                    "The tutor's file crashed twice on PyGAD 3: the fitness function needed 3 inputs, and "
                    "`plot_result()` is now `plot_fitness()`. Fixed both (marked *my fix*).",
                    "PyGAD warns that `keep_elitism` (default 1) overrides the sheet's `keep_parents=1`.",
                ],
            },
            {
                "task": "Tuning the GA",
                "task_note": "My experiment",
                "did": [
                    "Ran 8 different settings with 20 seeds each and compared the median error |output − 44| "
                    "(table + Fig 10.2).",
                    "Best: 200 generations + 50 per population – median error **0.0003**, all 20 runs within 0.01 "
                    "(sheet settings: 0.0073, 14/20). Worst: mutating 50% of the genes – 0.0294, 6/20.",
                ],
                "time": "1 h",
                "learning": [
                    "A GA is random, so you have to compare settings over many runs, not one.",
                    "More solutions and more generations help but cost time (9.4 s vs 0.7 s for 20 runs). Too much "
                    "mutation just wrecks good answers.",
                    "Steady-state selection (the sheet's choice) beat tournament and roulette wheel here.",
                ],
                "problems": [],
            },
            {
                "task": "8 Queen puzzle",
                "task_note": "Sheet part 3, `8_queen_puzzle.py`",
                "did": [
                    "Each answer = 8 numbers, the column of the queen in each row. Fitness = 1 / attacks, or 1.1 for "
                    "0 attacks.",
                    "The app crashed as soon as I pressed **Initial Population** (`delay_after_gen` was removed from "
                    "PyGAD), and **Start GA** froze the window. Fixed both.",
                    "Found a bug in the attack counting: all 8 queens on one diagonal (28 attacking pairs) came out as "
                    "**126**. Fixed it.",
                    "Ran the app's GA 30 times without the GUI: it found a 0-attack board **20/30** times (median 55 "
                    "generations). With the original counting it was only 14/30 (Fig 10.3, 10.4).",
                ],
                "time": "1.5 h",
                "learning": [
                    "The GA can still solve it with a wrong fitness (0 attacks is still 0), but a wrong count "
                    "ranks the other boards badly, so it finds the answer less often.",
                    "It doesn't always find the solution in 100 generations – the sheet says this too.",
                ],
                "problems": [
                    "Three crashes/bugs in the tutor's app (details in the table below).",
                    "In the app the genes become decimals like 3.7 after crossover and mutation – the board just "
                    "rounds them down.",
                ],
            },
            {
                "task": "Better encodings",
                "task_note": "My experiment",
                "did": [
                    "**Integer genes** (`gene_space=range(8)`): 13/30 – no better.",
                    "**Permutation** (every column used exactly once, swap mutation): **30/30**, median 1 generation, "
                    "0.1 s per run.",
                ],
                "time": "0.5 h",
                "learning": [
                    "How you write the answer down matters more than the GA settings: with a permutation, column "
                    "attacks are impossible, so only the diagonals are left to fix.",
                    "Part of it is luck: 8 of the 30 random starting populations already contained a solution "
                    "(0 of 30 for the app's style). The rest still got solved in a few generations.",
                ],
                "problems": [],
            },
        ],
        "total_time": "4.5 h",
        "total_note": "+ ~30 min laptop runs & screenshots",
        "screenshots_intro": "Figures 10.1–10.4 come straight out of my notebook. The yellow boxes are screenshots I "
                             "still need to take on my laptop. Set-up first: in the terminal, in the LabChallenge "
                             "folder, run `source .venv/bin/activate` then `pip install pygad kivy` (Windows: "
                             "`.venv\\Scripts\\activate`). Then `cd \"Lab 10\"` and do the steps below.",
        "figures": [
            {"path": "Lab 10/figures/10_1_linear_fitness.png", "width": 5.0,
             "caption": "linear model – best fitness each generation (sheet settings, log scale)"},
            {"path": "Lab 10/figures/10_2_linear_tuning.png", "width": 5.6,
             "caption": "linear model – median error over 20 runs for each setting (lower = better)"},
            {"path": "Lab 10/figures/10_3_queens_success.png", "width": 5.6,
             "caption": "8 Queens – how often each version found a 0-attack board in 30 runs"},
            {"path": "Lab 10/figures/10_4_queens_board.png", "width": 2.6,
             "caption": "one of the solutions the GA found: [4, 0, 7, 3, 1, 6, 2, 5]"},
        ],
        "screenshots": [
            {"id": "10.1", "title": "Terminal – PyGAD and Kivy installed",
             "what": "the end of `pip install pygad kivy` ('Successfully installed …' or 'Requirement already "
                     "satisfied'), then run `python -c \"import pygad; print(pygad.__version__)\"` and include the "
                     "version line.",
             "file": "Lab 10/screenshots/10.1_install.png"},
            {"id": "10.2", "title": "Linear model – output + fitness plot",
             "what": "run `python fitting_linear_model.py`. A plot window opens – take one shot of the plot, close it, "
                     "then a second shot of the terminal lines 'Parameters of the best solution … Predicted output … "
                     "Best fitness value reached after … generations'. Name them `10.2a_…` and `10.2b_…`.",
             "file": "Lab 10/screenshots/10.2_linear_model.png"},
            {"id": "10.3", "title": "8 Queens app – random starting board",
             "what": "run `python 8_queen_puzzle.py`, click **Initial Population**, then **Show Best Solution** – "
                     "screenshot the whole window (board with green 'Queen' squares and the 'Attacks = …' label).",
             "file": "Lab 10/screenshots/10.3_queens_start.png"},
            {"id": "10.4", "title": "8 Queens app – solved",
             "what": "click **Start GA** and wait until the label says 'Attacks = 0' (if it stops above 0 after 100 "
                     "generations, click Initial Population and Start GA again). Screenshot the window with the "
                     "solved board, plus the terminal with the last 'Generation = … / Fitness = 1.1' lines "
                     "(`10.4a_…` + `10.4b_…`).",
             "file": "Lab 10/screenshots/10.4_queens_solved.png"},
            {"id": "10.5", "title": "Notebook – tuning table",
             "what": "open `Lab10_Genetic_Algorithms.ipynb` in Jupyter (no need to re-run) and screenshot the tuning "
                     "table under 'My experiments – tuning the GA'.",
             "file": "Lab 10/screenshots/10.5_tuning_table.png"},
            {"id": "10.6", "title": "Notebook – 8 Queens results",
             "what": "in the same notebook, the 'original code says 126 attacks, fixed code says 28' lines and the "
                     "table with solved 14/30, 20/30, 13/30, 30/30.",
             "file": "Lab 10/screenshots/10.6_queens_table.png"},
            {"id": "10.7", "title": "My fixes in the code",
             "what": "`8_queen_puzzle.py` open in VS Code (or TextEdit) showing a couple of the lines marked "
                     "`(my fix)`, e.g. `pygadThread.start()` and `stop_criteria=\"reach_1.1\"`.",
             "file": "Lab 10/screenshots/10.7_my_fixes.png"},
        ],
        "notes": ["**Then:** save the screenshots in `Lab 10/screenshots/` with those names, and from the LabChallenge "
                  "folder run `python _tools/insert_screenshots.py 10`, `python _tools/tick_checklist.py 10 7 8 9 10` "
                  "and `python _tools/make_handin.py 10`."],
        "sections": [
            {
                "heading": "What I fixed in the tutor's programs (PyGAD 3)",
                "paragraphs": ["All changes are marked `(my fix)` in the code."],
                "table": {"header": ["File", "Problem", "My fix"], "rows": FIXES, "widths": [1700, 4165, 3100]},
            },
            {
                "heading": "Results – tuning the linear model (20 seeds per setting)",
                "table": {"header": ["Setting", "Median error", "Worst error", "Within 0.01"], "rows": TUNING,
                          "widths": [4165, 1600, 1600, 1600]},
            },
            {
                "heading": "Results – 8 Queens (30 runs each, max 100 generations)",
                "table": {"header": ["Version", "Found 0 attacks", "Median generations", "Time per run"],
                          "rows": QUEENS, "widths": [4165, 1800, 1500, 1500]},
            },
            {
                "heading": "Questions I asked myself",
                "qa": [(f"{i}. {q}", a) for i, (q, a) in enumerate(QA, 1)],
            },
        ],
    }
