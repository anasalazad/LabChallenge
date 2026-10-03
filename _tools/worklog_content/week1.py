# Week 1 worklog content - Lab 1 (LLM access: local Ollama + cloud Gemini)
# Markup: **bold**, `code`, [[yellow = still to fill in]].
# Everything here comes from Anas's own completed notebook: "Lab 1/Lab1_completed.ipynb"
# (latencies are the "Latency: …" lines it printed; Figure 1.1 is made from those numbers).
#     python _tools/build_worklogs.py 1

LOCAL, CLOUD = "Local – Ollama llama3.2:1b", "Cloud – Gemini gemini-3.5-flash"

COMPARISON = [
    ["Setup", "Install the Ollama app, download the model (~1.3 GB), `pip install ollama`. No account or key.",
     "Google account + API key from AI Studio, `pip install google-genai`. The key has to be kept secret."],
    ["Latency – count M/F in 20 rows", "**1.32 s**", "**3.18 s**"],
    ["Latency – apples, step by step", "**1.07 s**", "**2.09 s**"],
    ["Latency – apples, direct", "**0.91 s**", "**1.67 s**"],
    ["Cost", "Free – runs on my own laptop (uses my CPU and memory).",
     "Free on the free tier (daily limits); past that you pay per token."],
    ["Quality – counting", "**Wrong** – 8 F + 9 M (only 17 of 20), then swapped them around in its last sentence.",
     "**Right** – 11 F + 9 M = 20."],
    ["Quality – apples (31)", "Right with both prompts, short plain working.",
     "Right with both prompts, clearer step-by-step layout."],
    ["Quality – 'What is an intelligent system?'", "Long list, a bit generic – it even called 'self-awareness' "
     "a common feature.", "Well organised (perceive → reason → learn → act, examples, technologies) and accurate."],
    ["Privacy / offline", "Nothing leaves my laptop, works offline.", "My prompt goes to Google; needs internet."],
]

CHECKPOINT = [
    ("1. What's the practical difference in setup complexity between local and cloud?",
     "**Local:** install the Ollama app, download the model once (llama3.2:1b is about 1.3 GB), `pip install "
     "ollama` – then a few lines of code and it works. No account, no key, no limits and it even works offline, but "
     "it uses my laptop's memory and processor, so I can only run small models. **Cloud:** nothing to download, but "
     "I needed a Google account, an API key from AI Studio and `pip install google-genai`. The key has to stay "
     "secret (not typed into the notebook), and the free tier has limits."),
    ("2. Where did the two models disagree, and why might that happen?",
     ["On the counting task. Ollama said 8 female and 9 male (only 17 – there are 20 rows) and then swapped them "
      "in its last sentence. Gemini said 11 female and 9 male = 20, which is right. The local model only has about "
      "1 billion parameters, and LLMs don't really count – they read the list as tokens and guess the numbers, so "
      "a small model gets it wrong easily. Gemini is much bigger and thinks before it answers. (For counting, "
      "`df['sex'].value_counts()` in pandas is the reliable way.)",
      "On the apple question they agreed – both got 31 with and without 'think step by step'."]),
]


def build_spec():
    return {
        "week": 1,
        "dates": "2–9 August 2026",
        "student_name": "Anas Al Azad",
        "student_id": "105694136",
        "title": "Week 1 – Introduction to LLM access (local Ollama + cloud Gemini)",
        "intro": "My checklist for this week – ticked = done, unticked = still to do. My notebook is "
                 "`Lab 1/Lab1_completed.ipynb` in my repo.",
        "checklist": [
            ("Read the Week 1 sheet (LLM, API, Jupyter, local vs cloud)", True),
            ("Installed Ollama + downloaded `llama3.2:1b` (step 2)", True),
            ("Called the local model from Python with `ollama.chat` (steps 3–4)", True),
            ("Gemini API key + the same question in the cloud with `google-genai` (step 5)", True),
            ("Small dataset (`student-mat.csv`, 20 rows) + the same prompt on both models, timed with "
             "`time.time()` (steps 6–7)", True),
            ("'Think step by step' vs direct prompt on both models (step 8)", True),
            ("Gradio chat demo (step 9)", True),
            ("Deliverable: comparison table (latency, cost, quality) + checkpoint answers", True),
            ("Took the API key out of the notebook I hand in", True),
            ("Screenshots added (yellow boxes below)", False),
        ],
        "rows": [
            {
                "task": "Getting started",
                "task_note": "Step 1 + setup",
                "did": [
                    "Read the sheet: what an LLM, an API and a Jupyter notebook are, and running a model locally vs "
                    "in the cloud.",
                    "Made a separate Python environment for this lab (`ollama_venv`) and installed `ollama`, "
                    "`google-genai`, `pandas` and `gradio`.",
                ],
                "time": "0.5 h",
                "learning": [
                    "An LLM basically keeps guessing the next word – that's how it 'answers'.",
                    "An API is just a way for my code to send a request (the prompt) and get a response back.",
                ],
                "problems": [],
            },
            {
                "task": "Local model – Ollama",
                "task_note": "Steps 2–4",
                "did": [
                    "Installed Ollama and downloaded the small `llama3.2:1b` model.",
                    "Called it from my notebook with `ollama.chat(...)` and asked 'What is an intelligent system?' – "
                    "it answered with a long list of types, characteristics, uses and examples.",
                ],
                "time": "1 h",
                "learning": [
                    "Ollama runs a little server on my own laptop (localhost). The `ollama` library just sends my "
                    "prompt to it and gets the answer back as JSON – nothing leaves my computer.",
                    "The model file is loaded into memory the first time, so the first call is the slowest.",
                ],
                "problems": [
                    "The small model's answer was a bit generic and not always right – it listed 'self-awareness' "
                    "as a common characteristic of intelligent systems.",
                ],
            },
            {
                "task": "Cloud model – Gemini",
                "task_note": "Step 5",
                "did": [
                    "Made a free API key in Google AI Studio and installed `google-genai`.",
                    "Asked `gemini-3.5-flash` the same question – a well organised answer (perceive → reason → "
                    "learn → act, key characteristics, real examples, the technologies behind it).",
                ],
                "time": "0.5 h",
                "learning": [
                    "Cloud = nothing to download and a much bigger model, but every request goes over the internet "
                    "and needs the key.",
                ],
                "problems": [
                    "I first typed the API key straight into the notebook. That's not safe (anyone who sees the "
                    "notebook or my GitHub can use it), so I took it out of the copy I hand in – it should come from "
                    "an environment variable / `.env` file instead.",
                ],
            },
            {
                "task": "Same prompt on both models",
                "task_note": "Steps 6–7, `student-mat.csv`",
                "did": [
                    "Loaded `student-mat.csv` (student performance data) with pandas and kept the first 20 rows "
                    "like the sheet does.",
                    "Asked both models how many Male and Female students are in the `sex` column, with a "
                    "`time.time()` wrapper inside each function to log the latency.",
                    "**Ollama: 1.32 s** – said 8 F and 9 M (only 17 of 20) and then swapped them in its last "
                    "sentence. **Gemini: 3.18 s** – 11 F and 9 M = 20, which is right (Fig 1.1).",
                ],
                "time": "1 h",
                "learning": [
                    "Local was faster here (no internet in between), but fast and wrong isn't much use.",
                    "LLMs don't really count – they read the list as tokens. For counting, pandas "
                    "(`value_counts()`) is the right tool.",
                ],
                "problems": [
                    "The local model got the count wrong and contradicted itself in the same answer.",
                ],
            },
            {
                "task": "Think step by step vs direct",
                "task_note": "Step 8",
                "did": [
                    "Asked the apple question (3 boxes of 12, 5 rotten) once with 'Think step by step, then give your "
                    "final answer' and once without it, on both models.",
                    "All four answers were **31** (right). Ollama: 1.07 s step by step vs 0.91 s direct. Gemini: "
                    "2.09 s vs 1.67 s.",
                ],
                "time": "0.5 h",
                "learning": [
                    "For an easy question it made no difference to the answer – both models explained their working "
                    "even without being asked. The direct prompt was just a bit faster.",
                    "My 'direct' prompt only left out 'think step by step'. Asking for 'the number only' would "
                    "probably show a bigger difference.",
                ],
                "problems": [],
            },
            {
                "task": "Chat demo with Gradio",
                "task_note": "Step 9",
                "did": [
                    "Made a chat page with Gradio's `ChatInterface` ('Week 1: Local LLM Chat (Ollama)') that sends "
                    "my message to the local model.",
                ],
                "time": "0.5 h",
                "learning": [
                    "Gradio turns a normal Python function into a web page in a few lines.",
                ],
                "problems": [
                    "My function only sends the newest message (it ignores `history`), so the chat doesn't remember "
                    "what I said before – I'd have to pass the history to `ollama.chat` for that.",
                    "Importing gradio printed a 'TqdmWarning: IProgress not found' – harmless.",
                    "The sheet says `GradioUI`, but that's from smolagents (next week), so I used Gradio's own "
                    "`ChatInterface`.",
                ],
            },
            {
                "task": "Deliverable + checkpoint questions",
                "task_note": "Comparison table",
                "did": [
                    "Made the comparison table (latency, cost, output quality) from my own numbers and answered the "
                    "two checkpoint questions – both are below the screenshots.",
                ],
                "time": "0.5 h",
                "learning": [
                    "Local wins on cost, privacy and (here) speed; cloud wins on quality.",
                ],
                "problems": [],
            },
        ],
        "total_time": "4.5 h",
        "total_note": "+ ~20 min for screenshots",
        "screenshots_intro": "Figure 1.1 is made from the latencies my notebook printed. The yellow boxes are "
                             "screenshots I still need to add (take them from `Lab1_completed.ipynb` – the "
                             "copy without the API key).",
        "figures": [
            {"path": "Lab 1/figures/1_1_latency.png", "width": 5.8,
             "caption": "latency per call for each task, local vs cloud (from my time.time() wrapper)"},
        ],
        "screenshots": [
            {"id": "1.1", "title": "Terminal – ollama run llama3.2:1b",
             "what": "the terminal after `ollama run llama3.2:1b` and the model's reply when you type `hello` "
                     "(`/bye` to quit).",
             "file": "Lab 1/screenshots/1.1_ollama_cli.png"},
            {"id": "1.2", "title": "Notebook – local model",
             "what": "the `import ollama` + `ollama.chat(...)` cells and the start of the answer to 'What is an "
                     "intelligent system?'.",
             "file": "Lab 1/screenshots/1.2_ollama_notebook.png"},
            {"id": "1.3", "title": "Google AI Studio – my API key",
             "what": "aistudio.google.com/app/api-keys with your key in the list (it only shows the last few "
                     "characters – that's fine). Never the full key.",
             "file": "Lab 1/screenshots/1.3_ai_studio_key.png"},
            {"id": "1.4", "title": "Notebook – Gemini call",
             "what": "the `genai.Client()` + `generate_content` cells and the start of Gemini's answer – from "
                     "`Lab1_completed.ipynb`, so no key is visible.",
             "file": "Lab 1/screenshots/1.4_gemini_notebook.png"},
            {"id": "1.5", "title": "Notebook – counting on both models",
             "what": "the two counting functions' 'Latency: 1.32s' / 'Latency: 3.18s' lines and both answers. Two "
                     "shots are fine: `1.5a_…` + `1.5b_…`.",
             "file": "Lab 1/screenshots/1.5_count_both_models.png"},
            {"id": "1.6", "title": "Notebook – step by step vs direct",
             "what": "the four apple cells with their 'Latency' lines and answers (Ollama + Gemini, reasoning + "
                     "non-reasoning). Two shots are fine: `1.6a_…` + `1.6b_…`.",
             "file": "Lab 1/screenshots/1.6_reasoning.png"},
            {"id": "1.7", "title": "Gradio chat in the browser",
             "what": "the 'Week 1: Local LLM Chat (Ollama)' page (http://127.0.0.1:7860) after asking it something.",
             "file": "Lab 1/screenshots/1.7_gradio_chat.png"},
            {"id": "1.8", "title": "Notebook – checkpoint answers + comparison table",
             "what": "the 'Checkpoint Questions' cell at the end of the notebook with the comparison table.",
             "file": "Lab 1/screenshots/1.8_comparison_table.png"},
        ],
        "sections": [
            {
                "heading": "Deliverable – comparison table (latency, cost, output quality)",
                "paragraphs": ["From my notebook run – latencies are what my `time.time()` wrapper printed."],
                "table": {"header": ["", LOCAL, CLOUD], "rows": COMPARISON, "widths": [2165, 3400, 3400]},
            },
            {
                "heading": "Checkpoint questions",
                "qa": CHECKPOINT,
            },
        ],
    }
