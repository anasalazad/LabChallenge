# Week 1 worklog content - Lab 1 (LLM access: local Ollama + cloud Gemini)
# Markup: **bold**, `code`, [[yellow = filled in once the notebook has run]].
# Numbers come from "Lab 1/results/lab1_results.json" (saved by Lab1_LLM_Access.ipynb).
# Run the notebook, then:  python _tools/build_worklogs.py 1

from worklog_content._results import fig, get, has, k, load, v

RESULTS = "Lab 1/results/lab1_results.json"


def _right(r, backend, prompt):
    runs = get(r, f"reasoning.{backend}.{prompt}")
    if not runs:
        return None, None
    return sum(x["correct"] for x in runs), len(runs)


def build_spec():
    r = load(RESULTS)
    ran = bool(r)
    n = k(r, "sentiment.n", 20)
    gm = k(r, "gemini_model_used", "gemini-3.5-flash")

    # ---- sentences that depend on the run ---------------------------------
    o_avg, g_avg = get(r, "sentiment.ollama.avg_s"), get(r, "sentiment.gemini.avg_s")
    if o_avg is not None and g_avg is not None:
        if o_avg < g_avg:
            speed = (f"On my laptop the local model was actually quicker per review ({o_avg} s vs {g_avg} s) – "
                     "no internet round trip, and a 1-word answer is quick to write.")
        else:
            speed = (f"Gemini was quicker per review ({g_avg} s vs {o_avg} s) even with the internet in between – "
                     "Google's hardware is just much faster than my laptop.")
    else:
        speed = "[[which one was faster per review, and by how much]]"

    so, no_ = _right(r, "ollama", "step by step")
    do, _ = _right(r, "ollama", "direct")
    sg, ng = _right(r, "gemini", "step by step")
    dg, _ = _right(r, "gemini", "direct")
    if so is None:
        reason_result = ("Local model (3 tries each): step by step [[x]]/3 right, direct [[y]]/3. "
                         "Gemini: step by step [[x]]/1, direct [[y]]/1.")
        reason_learning = "[[did 'think step by step' help the small model? (see the summary table in step 8)]]"
    else:
        reason_result = (f"Local model ({no_} tries each): step by step **{so}/{no_}** right, direct **{do}/{no_}**. "
                         f"Gemini: step by step **{sg}/{ng}**, direct **{dg}/{ng}**.")
        if so > do:
            reason_learning = (f"Making the small model write out its working really helped ({so}/{no_} vs {do}/{no_}) – "
                               "it has to do 3 × 12 first and then take away 5, instead of guessing a number.")
        elif so == do:
            reason_learning = (f"For this easy question it didn't change much for the local model ({so}/{no_} both ways).")
        else:
            reason_learning = (f"Surprisingly the direct prompt did better for the local model here ({do}/{no_} vs "
                               f"{so}/{no_}) – a 1B model can talk itself into a wrong answer.")
        if sg == ng and dg == ng:
            reason_learning += " Gemini got it right both ways – it already 'thinks' inside before it answers."
    w_step = get(r, "reasoning.ollama.step by step")
    w_dir = get(r, "reasoning.ollama.direct")
    if w_step and w_dir:
        ws = round(sum(x["words"] for x in w_step) / len(w_step))
        wd = round(sum(x["words"] for x in w_dir) / len(w_dir))
        words_line = (f"The step-by-step answers are much longer (about {ws} words vs {wd}), so they take longer "
                      "and would cost more on a paid plan.")
    else:
        words_line = "Step-by-step answers are longer, so they take longer and cost more tokens on a paid plan."

    gemini_problems = []
    probs = get(r, "gemini_problems", []) or []
    n429 = sum("429" in p for p in probs)
    switched = [p for p in probs if "switched" in p]
    if n429:
        gemini_problems.append(f"Gemini's free tier said 'too many requests' (error 429) {n429} time(s) – my helper "
                               "waits and tries again, so the run still finished.")
    for p in switched:
        gemini_problems.append(f"Model problem: {p}.")

    all_line = ""
    if has(r, "ollama_all.n"):
        all_line = (f"Extra: since local is free, I also ran it on all {r['ollama_all']['n']} reviews – "
                    f"{r['ollama_all']['accuracy']:.0%} said Negative ({r['ollama_all']['seconds']:.0f} s in total).")

    # ---- comparison table (deliverable) --------------------------------------
    if has(r, "comparison_rows"):
        comp_rows = [list(row) for row in r["comparison_rows"]]
    else:
        comp_rows = [
            ["Setup", "install the Ollama app + download the model (~1.3 GB), no account or key",
             "Google account + API key kept in `.env`, install `google-genai`"],
            ["Latency – 'What is an intelligent system?'", "[[x.x s]]", "[[x.x s]]"],
            ["Latency – sentiment, 20 reviews", "[[avg x.x s/review]]", "[[avg x.x s/review]]"],
            ["Cost", "$0 – runs on my laptop", "$0 on the free tier (limited requests per day) – [[tokens used]]"],
            ["Quality – sentiment (all 20 are negative)", "[[x/20 right]]", "[[x/20 right]]"],
            ["Quality – apples question (31)", "[[step by step x/3, direct x/3]]", "[[step by step x/1, direct x/1]]"],
            ["Privacy / offline", "nothing leaves my laptop, works offline", "reviews are sent to Google, needs internet"],
        ]

    q2 = get(r, "checkpoint_q2") or ("[[run the notebook – the answer is printed under the last cell "
                                     "(which reviews they disagreed on and why)]]")

    return {
        "week": 1,
        "dates": "2–9 August 2026",
        "student_name": "Anas Al Azad",
        "student_id": "105694136",
        "title": "Week 1 – Introduction to LLM access (local Ollama + cloud Gemini)",
        "intro": "My checklist for this week – ticked = done, unticked = still to do. Everything is in "
                 "`Lab 1/Lab1_LLM_Access.ipynb` in my repo." + ("" if ran else
                 " (Yellow bits fill in by themselves once I've run the notebook and rebuilt this worklog.)"),
        "checklist": [
            ("Read the Week 1 sheet + wrote the basics (LLM, API, Jupyter, local vs cloud) in my own words", True),
            ("Notebook `Lab1_LLM_Access.ipynb` set up for all 9 steps", True),
            ("Installed Ollama + ran `llama3.2:1b` in the terminal (step 2)", has(r, "hello.ollama")),
            ("Called the local model from Python + looked at what happens under the hood (steps 3–4)",
             has(r, "under_hood")),
            ("Gemini API key (kept in `.env`) + the same prompt in the cloud (step 5)", has(r, "hello.gemini")),
            ("Loaded `reviews.csv` + ran the same prompts on both models with a `time.time()` wrapper (steps 6–7)",
             has(r, "sentiment")),
            ("'Think step by step' vs direct answer (step 8)", has(r, "reasoning")),
            ("Gradio chat demo (step 9)", has(r, "gradio")),
            ("Deliverable: comparison table (latency, cost, quality) + checkpoint answers", has(r, "comparison_rows")),
            ("Screenshots added (yellow boxes below)", False),
        ],
        "rows": [
            {
                "task": "Getting started",
                "task_note": "Step 1 + setup",
                "did": [
                    "Read the sheet and wrote down in my own words what an LLM, an API and a Jupyter notebook are, "
                    "and what the difference is between running a model locally and in the cloud (top of my notebook).",
                    "Made a Python virtual environment and installed `ollama`, `google-genai`, `pandas`, `gradio` "
                    "and `python-dotenv`.",
                ],
                "time": "0.5 h",
                "learning": [
                    "An LLM basically keeps guessing the next word – that's how it 'answers'.",
                    "An API is just a way for my code to send a request (the prompt) and get a response (the answer).",
                ],
                "problems": [],
            },
            {
                "task": "Local model – Ollama",
                "task_note": "Steps 2–4",
                "did": [
                    "Installed the Ollama app and ran `ollama run llama3.2:1b` in the terminal – it downloaded the "
                    f"model ({k(r, 'under_hood.disk_gb', '1.3')} GB) and I could chat with it straight away.",
                    "Called it from my notebook with `ollama.chat()` – 'What is an intelligent system?' took "
                    f"{v(r, 'hello.ollama.seconds', placeholder='x.x')} s.",
                    "Looked under the hood: sent the same kind of request by hand with `requests.post` to "
                    f"`localhost:11434` and got plain JSON back (status {k(r, 'under_hood.http_status', 200)}).",
                ],
                "time": "1 h",
                "learning": [
                    "Ollama is a little web server running on my own laptop – the Python library just sends it requests.",
                    f"The model is {k(r, 'under_hood.params', '1.2B')} parameters squeezed down to 8 bits "
                    f"({k(r, 'under_hood.quant', 'Q8_0')}) so it fits in about "
                    f"{v(r, 'under_hood.mem_gb', placeholder='x')} GB of memory. It wrote about "
                    f"{v(r, 'hello.ollama.tok_per_s', placeholder='xx')} tokens a second on my laptop.",
                    "The first call is the slowest because the model has to be loaded into memory first.",
                ],
                "problems": [],
            },
            {
                "task": "Cloud model – Gemini",
                "task_note": "Step 5",
                "did": [
                    "Made a free API key in Google AI Studio and put it in a `.env` file (git ignores it) instead of "
                    "typing it into the code like the sheet does.",
                    f"Ran the same question on `{gm}` – took {v(r, 'hello.gemini.seconds', placeholder='x.x')} s and gave "
                    f"a {v(r, 'hello.gemini.answer_words', placeholder='xxx')}-word answer (local: "
                    f"{v(r, 'hello.ollama.answer_words', placeholder='xxx')} words).",
                ],
                "time": "0.5 h",
                "learning": [
                    "Cloud = nothing to download and a much bigger model, but every request goes over the internet "
                    "and needs the key – so the key has to stay secret.",
                    "Gemini 'thinks' before it answers even if you don't ask – "
                    f"{v(r, 'hello.gemini.thinking_tokens', placeholder='xxx')} hidden thinking tokens on this "
                    "question, which also count towards your usage.",
                ],
                "problems": [
                    "A yellow warning about 'automatic function calling' came up on the first Gemini call – it's just "
                    "the library being chatty, nothing broke.",
                ] + gemini_problems,
            },
            {
                "task": "Same prompts on both models",
                "task_note": "Steps 6–7, `reviews.csv`",
                "did": [
                    f"Loaded `reviews.csv` – {k(r, 'dataset.rows', 99)} movie reviews, about "
                    f"{k(r, 'dataset.avg_words', 213)} words each.",
                    f"Ran the sheet's sentiment prompt on the first {n} reviews with both models, with a "
                    "`time.time()` wrapper logging every single call.",
                    f"Local: {v(r, 'sentiment.ollama.avg_s', placeholder='x.x')} s per review on average, "
                    f"**{v(r, 'sentiment.ollama.correct', placeholder='x')}/{n}** right, "
                    f"{v(r, 'sentiment.ollama.one_word', placeholder='x')}/{n} answered with one word. "
                    f"Cloud: {v(r, 'sentiment.gemini.avg_s', placeholder='x.x')} s, "
                    f"**{v(r, 'sentiment.gemini.correct', placeholder='x')}/{n}** right, "
                    f"{v(r, 'sentiment.gemini.one_word', placeholder='x')}/{n} one word.",
                    f"The two models agreed on {v(r, 'sentiment.agree', placeholder='x')}/{n} reviews (Fig 1.1). "
                    + all_line,
                ],
                "time": "1 h",
                "learning": [
                    speed,
                    "A wrapper (decorator) is an easy way to time every call without touching the function itself.",
                ],
                "problems": [
                    "The sheet's code uses `df['text']` but the column is called `Text` → `KeyError: 'text'`. "
                    "Renamed the columns after loading.",
                    "Every review in the file is labelled 0 (negative), so I can only check how often each model "
                    "says Negative – I'd need some positive reviews to test it properly.",
                    f"{k(r, 'dataset.broken_chars', 5)} reviews have broken characters (e.g. 'clich√©' instead of 'cliché') from a bad text "
                    "encoding – left them as they are.",
                ],
            },
            {
                "task": "Think step by step vs direct",
                "task_note": "Step 8",
                "did": [
                    "Asked the apple question (3 boxes of 12, 5 rotten → **31**) once with the sheet's "
                    "'think step by step' prompt and once with a direct 'final number only' prompt.",
                    reason_result,
                ],
                "time": "0.5 h",
                "learning": [reason_learning, words_line],
                "problems": [],
            },
            {
                "task": "Chat demo with Gradio",
                "task_note": "Step 9",
                "did": [
                    "Made a chat window with Gradio's `ChatInterface` and a switch to pick the local or the cloud "
                    "model. Every answer shows which model replied and how long it took.",
                    "It sends the whole conversation each time, so the model remembers what I said before.",
                ],
                "time": "0.5 h",
                "learning": [
                    "Gradio turns a normal Python function into a web page in a few lines.",
                    "The model itself doesn't remember anything – the 'memory' is just my code sending the old "
                    "messages again.",
                ],
                "problems": [
                    "The sheet says `GradioUI`, but that's from smolagents (next week) and there's no agent yet, "
                    "so I used Gradio's own `ChatInterface`.",
                ],
            },
            {
                "task": "Deliverable + checkpoint questions",
                "task_note": "Comparison table",
                "did": [
                    "Comparison table (latency, cost, output quality) made from my own numbers, and answered the two "
                    "checkpoint questions – both are below the screenshots.",
                ],
                "time": "0.5 h",
                "learning": [
                    "Local wins on cost and privacy, cloud wins on quality and how easy it is to use a big model.",
                ],
                "problems": [],
            },
        ],
        "total_time": "4.5 h",
        "total_note": "+ ~20 min for screenshots",
        "screenshots_intro": "Figure 1.1 comes straight out of my notebook. The yellow boxes are screenshots I still "
                             "need to add.",
        "figures": [
            fig("Lab 1/figures/1_1_latency_and_answers.png",
                "seconds per review for each model (left) and what each model answered (right)", 6.3),
        ],
        "screenshots": [
            {"id": "1.1", "title": "Terminal – `ollama run llama3.2:1b`",
             "what": "the terminal after `ollama run llama3.2:1b`: the 'pulling … success' lines and the model's "
                     "reply after you type `hello`.",
             "file": "Lab 1/screenshots/1.1_ollama_cli.png"},
            {"id": "1.2", "title": "Notebook – local model + under the hood",
             "what": "the step 3 cell (`ollama.chat`) with its answer and the '--- llama3.2:1b: … s' line, and the "
                     "step 4 output (HTTP status 200, the JSON keys, 'loaded in memory'). Two shots are fine: "
                     "`1.2a_…` + `1.2b_…`.",
             "file": "Lab 1/screenshots/1.2_ollama_notebook.png"},
            {"id": "1.3", "title": "Google AI Studio – my API key",
             "what": "aistudio.google.com/app/api-keys with your key in the list (it only shows the last few "
                     "characters – that's fine). Never screenshot the full key.",
             "file": "Lab 1/screenshots/1.3_ai_studio_key.png"},
            {"id": "1.4", "title": "Notebook – Gemini call",
             "what": "the step 5 output: Gemini's answer, the '--- gemini… s | prompt … tokens' line and the "
                     "'Same question: local … vs cloud …' line.",
             "file": "Lab 1/screenshots/1.4_gemini_notebook.png"},
            {"id": "1.5", "title": "Notebook – sentiment on both models",
             "what": "the step 7 results table (avg seconds, correct, one-word answers, predictions) and the "
                     "'agreed on …' lines under it.",
             "file": "Lab 1/screenshots/1.5_sentiment_results.png"},
            {"id": "1.6", "title": "Notebook – step by step vs direct",
             "what": "the bottom of the step 8 cell: one or two answers + the small summary table "
                     "(right / avg seconds / avg words).",
             "file": "Lab 1/screenshots/1.6_reasoning.png"},
            {"id": "1.7", "title": "Gradio chat in the browser",
             "what": "http://127.0.0.1:7860 with one question answered by the local model and one by Gemini "
                     "(switch the 'Which model answers?' button in between) – the '(model, x s)' line under each "
                     "answer should show.",
             "file": "Lab 1/screenshots/1.7_gradio_chat.png"},
            {"id": "1.8", "title": "Notebook – comparison table",
             "what": "the 'Deliverable – comparison table' output and the checkpoint question 2 answer under it.",
             "file": "Lab 1/screenshots/1.8_comparison_table.png"},
        ],
        "sections": [
            {
                "heading": "Deliverable – comparison table (latency, cost, output quality)",
                "paragraphs": ["Made from the numbers in my notebook run" +
                               (f" ({r.get('run_at')}, local `llama3.2:1b` vs cloud `{gm}`)." if ran else ".")],
                "table": {"header": ["", "Local – Ollama llama3.2:1b", f"Cloud – Gemini {gm}"],
                          "rows": comp_rows, "widths": [2165, 3400, 3400]},
            },
            {
                "heading": "Checkpoint questions",
                "qa": [
                    ("1. What's the practical difference in setup complexity between local and cloud?",
                     "Local: install one app and download the model once, then it just works – no account, no key, "
                     "no limits and it even works offline. The catch is it uses my laptop's memory, it's only as fast "
                     "as my laptop and I can only run small models. Cloud: nothing to download and a much bigger "
                     "model, but I needed a Google account and an API key that I have to keep secret (in `.env`, "
                     "never in the code or a screenshot), and I have to live with the free-tier limits."),
                    ("2. Where did the two models disagree, and why might that happen?", q2),
                ],
            },
        ],
    }
