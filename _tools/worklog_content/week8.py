# Week 8 worklog content - Lab 8 (RNN, LSTM/GRU, Attention) + deliverable
# Markup: **bold**, `code`. Edit text here, then: python _tools/build_worklogs.py 8

SPEC = {
    "week": 8,
    "dates": "1-7 October 2026",
    "student_name": "Anas Al Azad",
    "student_id": "",
    "title": "Week 8 – RNN, LSTM/GRU and Attention (+ Lab 8 deliverable)",
    "intro": "My checklist for this week – ticked = done (notebook, plots and my one-page summary are "
             "in the **Lab 8** folder of my repo), unticked = still on my to-do list.",
    "checklist": [
        ("Read the Lab 8 sheet (sequence data, RNN, LSTM/GRU, attention + positional encoding, the "
         "“remember the first digit” task)", True),
        ("Setup + **Part 1**: measured the vanishing gradient for RNN / LSTM / GRU (gradient plot)", True),
        ("**Part 2**: trained RNN / LSTM / GRU for T = 5, 10, 20, 60 with 3 seeds each", True),
        ("Part 2 experiment: hidden layer 32 → 128 units at T = 20", True),
        ("**Part 3**: self-attention for T = 10, 20, 60 + plotted where it looks (attention weights)", True),
        ("Part 3 ablation: removed positional encoding", True),
        ("Results table (model × T) + answered the 3 checkpoint questions", True),
        ("Deliverable: one-page summary (`Lab8_Summary.docx` / `.pdf`)", True),
        ("Extra: 40 epochs instead of 15 at T = 20 (memory limit or just training?)", True),
        ("Put my student ID on the summary and export it to PDF again", False),
        ("Open / re-run the notebook on my laptop and take the screenshots", False),
        ("Hand in the notebook + one-page summary", False),
        ("Add my screenshots (yellow boxes below)", False),
    ],
    "rows": [
        {
            "task": "Theory – sequences & memory",
            "task_note": "Lab 8 sheet sections 1–2",
            "did": [
                "Read how an RNN keeps a hidden state, why early info fades (vanishing gradient), how "
                "LSTM/GRU add gates + a cell state, and how attention links any two steps directly but "
                "needs positional encoding and costs O(T²).",
                "Understood the test task: sequences of T random digits, label = the **first** digit, "
                "so accuracy only measures memory (chance = 0.10).",
            ],
            "time": "1 h",
            "learning": [
                "Hidden state = the RNN's memory, overwritten every step.",
                "Gates = learned switches for what to write / keep / forget.",
                "Attention is parallel and has no distance problem, but doesn't know order by itself.",
            ],
            "problems": [],
        },
        {
            "task": "Part 1 – vanishing gradients",
            "task_note": "`Lab8_RNN_LSTM_Attention.ipynb`",
            "did": [
                "Ran the setup (3 sequences of 10 digits + labels ✔) and the gradient cell: fed a "
                "50-step random sequence through each layer and measured the gradient at every input step.",
                "Gradient at the last step / first step: **RNN 1.5e+13, LSTM 7.8e+10, GRU 2.8e+10** "
                "(Fig 8.1) – same as the sheet's typical result.",
            ],
            "time": "0.5 h",
            "learning": [
                "The gradient shrinks exponentially going back in time – a straight line on a log plot.",
                "Gates help (LSTM/GRU shrink ~100× less) but don't fix it.",
            ],
            "problems": [],
        },
        {
            "task": "Part 2 – RNN vs LSTM vs GRU",
            "task_note": "3 models × 4 lengths × 3 seeds",
            "did": [
                "Trained all 36 models (15 epochs each) – took 212 s on CPU (sheet said ~5 min).",
                "Mean accuracy for T = 5 / 10 / 20 / 60: **RNN 1.00 / 0.66 / 0.10 / 0.10, "
                "LSTM 1.00 / 0.96 / 0.47 / 0.09, GRU 1.00 / 1.00 / 0.10 / 0.09** (Fig 8.3).",
                "Experiment 32 → 128 units at T = 20: RNN 0.77, LSTM 0.59, GRU **1.00** "
                "(sheet: 0.85 / 0.59 / 1.00).",
            ],
            "time": "1.5 h",
            "learning": [
                "All three are perfect at T = 5; the plain RNN breaks first, the gated ones hold on "
                "longer, but by T = 60 everything is at chance.",
                "A bigger hidden state helped a lot at T = 20 (GRU 0.10 → 1.00).",
            ],
            "problems": [
                "Same settings, different seeds = very different results (RNN at T = 10: 0.79 / 1.00 / "
                "0.19; LSTM at T = 20: 0.32 / 0.18 / 0.90) – had to look at all 3 runs, not just "
                "the mean.",
                "My RNN-128 result (0.77) is a bit lower than the sheet's 0.85 – probably a "
                "different CPU/PyTorch version; everything else matched exactly.",
            ],
        },
        {
            "task": "Part 3 – self-attention",
            "task_note": "+ attention plot + ablation",
            "did": [
                "Self-attention with positional encoding: **1.00 / 1.00 / 1.00** for T = 10 / 20 / 60 "
                "– even T = 60 is easy because step 1 is only one hop from the last step.",
                "Attention plot at T = 20: the last position puts **0.95 (head 0) and 0.80 (head 1)** "
                "of its weight on position 0 – it looks straight at the first digit (Fig 8.2).",
                "Ablation without positional encoding: **0.26** (T = 10) and **0.18** (T = 30).",
                "Worked out why: without order, the best possible guess is the most common digit in "
                "the sequence – I simulated that = 0.27 / 0.20, almost exactly what the model got.",
            ],
            "time": "1.5 h",
            "learning": [
                "Attention without positions = a bag of digits (permutation-invariant).",
                "Positional encoding (sin/cos) gives every step a unique tag – that's what "
                "Transformers/LLMs rely on.",
            ],
            "problems": [
                "The sheet doesn't say why the ablation lands at 0.26 instead of chance (0.10) – "
                "the model can still count the digits, it just can't tell which one came first "
                "(I checked this with a simulation, see above).",
            ],
        },
        {
            "task": "Deliverable + extra",
            "task_note": "`Lab8_Summary.pdf`, extra experiment",
            "did": [
                "Wrote the **one-page summary**: results table (Parts 2 + 3), gradient plot, attention "
                "plot and my answers to the 3 checkpoint questions (`make_summary.py` builds it from "
                "the notebook's `results.json`, so it updates if I re-run).",
                "Extra: 40 epochs instead of 15 at T = 20 → **LSTM 0.47 → 0.93, GRU 0.10 "
                "→ 0.96**, RNN 0.55 (one seed still stuck at 0.10).",
            ],
            "time": "1.5 h",
            "learning": [
                "At T = 20 it's partly a training problem: the gated models CAN learn the dependency, "
                "they just need many more updates because the signal from step 1 is so weak.",
            ],
            "problems": [
                "Fitting everything on ONE page – had to put the two plots side by side and keep "
                "each answer to 3 sentences.",
            ],
        },
    ],
    "total_time": "6 h",
    "total_note": "+ ~30 min screenshots & hand-in",
    "screenshots_intro": "Figures 8.1–8.3 come straight out of my `Lab8_RNN_LSTM_Attention.ipynb` "
                         "(8.1 and 8.2 are the two plots the deliverable asks for). The yellow boxes are "
                         "screenshots I still need to add.",
    "figures": [
        {"path": "Lab 8/figures/8_1_gradient_plot.png", "width": 4.6,
         "caption": "Part 1 – gradient size at each of the 50 input steps (log scale)"},
        {"path": "Lab 8/figures/8_2_attention_plot.png", "width": 5.6,
         "caption": "Part 3 – where the last position looks at T = 20 (averaged over 200 sequences)"},
        {"path": "Lab 8/figures/8_3_accuracy_vs_T.png", "width": 4.6,
         "caption": "mean test accuracy vs sequence length for every model (chance = 0.10)"},
    ],
    "screenshots": [
        {"id": "8.1", "title": "Notebook – setup + Part 1",
         "what": "the setup output (3 rows of 10 digits + the 3 labels) and the Part 1 cell with its 3 "
                 "ratio lines (1.5e+13 / 7.8e+10 / 2.8e+10) and the gradient plot.",
         "file": "Lab 8/screenshots/8.1_setup_and_part1.png"},
        {"id": "8.2", "title": "Notebook – Part 2 results",
         "what": "the 12 printed lines for rnn / lstm / gru × T = 5, 10, 20, 60 (+ “took …s”) "
                 "and the 3 lines of the 128-unit experiment.",
         "file": "Lab 8/screenshots/8.2_part2_results.png"},
        {"id": "8.3", "title": "Notebook – Part 3 attention",
         "what": "the attn lines (T = 10, 20, 60 all 1.00) and the attention plot with both heads.",
         "file": "Lab 8/screenshots/8.3_part3_attention.png"},
        {"id": "8.4", "title": "Notebook – ablation + results table",
         "what": "the attn_nopos lines (0.26 / 0.18) and the results table (model × T).",
         "file": "Lab 8/screenshots/8.4_ablation_and_table.png"},
        {"id": "8.5", "title": "My one-page summary",
         "what": "`Lab8_Summary.pdf` open on screen (whole page visible, with your student ID on it).",
         "file": "Lab 8/screenshots/8.5_summary_pdf.png"},
    ],
}
