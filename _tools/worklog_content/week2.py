# Week 2 worklog content - Lab 2 (smolagents: agent with tools and memory)
# Markup: **bold**, `code`, [[yellow = still to fill in]].
# Everything here comes from Anas's own completed notebook: "Lab 2/Lab2_completed.ipynb"
# (step times/tokens are the "[Step n: Duration … | Input tokens …]" lines smolagents printed;
# Figure 2.1 is made from those numbers).
#     python _tools/build_worklogs.py 2

CLOUD = "Cloud – Llama-3.3-70B (Hugging Face)"
LOCAL = "Local – Qwen2.5-1.5B (TransformersModel)"

COMPARISON = [
    ["Finished?", "**Yes** – final answer 795,000", "**No** – I stopped it after 16 steps"],
    ["Thought → Code → Observation cycles", "3 (search → calculate → final_answer)",
     "16 – step 1 searched, steps 2–15 were all 'Error in code parsing'"],
    ["Time", "about **6 s** (2.83 + 1.74 + 1.43 s)", "about **73 min** (105–362 s per step)"],
    ["Tokens in / out", "8,226 / 178", "76,950 / 1,128 (by step 15)"],
    ["Web searches", "1 (DuckDuckGo)", "1 (DuckDuckGo)"],
    ["Answer", "795,000 = 15% of 5.3 million (one of the numbers in the search results)",
     "none – its first try (5,350,705 × 0.15 = 802,605.75) was in the wrong code format"],
    ["Weather question (step 6)", "failed – '402 Payment Required', my free monthly HF credits were used up",
     "didn't run – the cell stopped at the cloud error"],
    ["Cost", "free monthly credits (and then they ran out)", "free – runs on my laptop's CPU"],
]

CHECKPOINT = [
    ("1. What did the framework do for you that you would have written manually in Week 1?",
     "In Week 1 I wrote every call myself: build the prompt, call the model, read the reply, time it. smolagents "
     "did all of that plus: it wrote a long system prompt that explains the tools and the Thought → Code → "
     "Observation format (you can see it inside `agent.memory.steps`), pulled the code out of the model's reply, "
     "ran it, sent back what it printed, sent back error messages so the model could fix them, kept looping until "
     "`final_answer()` was called, gave me a ready-made web search tool, recorded every step (time, tokens, code, "
     "output) in memory, and gave me a chat UI. Switching cloud ↔ local was one line."),
    ("2. How many Thought → Code → Observation cycles ran before the agent gave a final answer, and what triggered "
     "it to stop?",
     "Sum of 1 to 50: **2 cycles** (work it out, then answer). Melbourne task on the cloud model: **3 cycles** – "
     "search, calculate 15% of 5.3 million, then answer. It stopped because the code in the last cycle called "
     "`final_answer(...)` – that's the signal smolagents waits for. (The local model never called it properly, so "
     "it kept going until I stopped it.)"),
    ("3. What changed when you swapped from cloud to local, and what stayed the same?",
     "**Stayed the same:** the agent code, the DuckDuckGo tool, the task, the system prompt and the Thought → Code → "
     "Observation loop – only the `model=` line changed. **Changed:** speed (about 2 s per step in the cloud vs "
     "105–362 s on my laptop) and quality – the small model couldn't follow the required code format, and it didn't "
     "use any Hugging Face credits."),
    ("4. Did your local model complete the task successfully? If not, what did it get wrong?",
     "Not at home. The search worked, but then it wrote its code as a markdown block (between three back-quotes) "
     "instead of inside the `<code>…</code>` tags smolagents needs, 14 times in a row, so none of it ran – it kept 'answering' with a variable that never "
     "existed. I stopped it after 16 steps (about 73 minutes). Its first attempt (5,350,705 × 0.15) was actually "
     "fine, just in the wrong format. (In the lab session it did finish.) The '402 – credits used up' error in "
     "step 6 came from the cloud model, not the local one."),
]


def build_spec():
    return {
        "week": 2,
        "dates": "10–16 August 2026",
        "student_name": "Anas Al Azad",
        "student_id": "105694136",
        "title": "Week 2 – Agent with tools and memory (smolagents)",
        "intro": "My checklist for this week – ticked = done, unticked = still to do. My notebook is "
                 "`Lab 2/Lab2_completed.ipynb` in my repo.",
        "checklist": [
            ("Read the Week 2 sheet", True),
            ("Installed smolagents + made a Hugging Face token (step 1)", True),
            ("Basic cloud agent with no tools – sum of 1 to 50 (step 2)", True),
            ("DuckDuckGo search tool + two-step task (Melbourne population, then 15%) (step 3)", True),
            ("Looked inside `agent.memory.steps` (step 4)", True),
            ("Same task with the local `TransformersModel` (step 5) – ran, didn't finish", True),
            ("Cloud vs local with `run_and_time` (step 6) – blocked: free HF credits ran out (402)", False),
            ("Agent in `GradioUI` (step 7) – launched; fix the model name typo for a working reply", False),
            ("Answered the 4 checkpoint questions", True),
            ("Class notes – agent architecture & design patterns", True),
            ("Took the HF token out of the notebook I hand in", True),
            ("Screenshots added (yellow boxes below)", False),
        ],
        "rows": [
            {
                "task": "Setup",
                "task_note": "Step 1",
                "did": [
                    "Installed `smolagents` (with the toolkit and transformers extras) in my `ollama_venv` "
                    "environment and made a free Hugging Face access token.",
                ],
                "time": "0.5 h",
                "learning": [
                    "A framework like smolagents runs the 'ask the model → use a tool → ask again' loop for me.",
                ],
                "problems": [
                    "I typed the HF token straight into the notebook (three cells). Anyone who sees it could use my "
                    "account, so I took it out of the copy I hand in – it should come from the `HF_TOKEN` "
                    "environment variable.",
                    "Importing smolagents printed a 'TqdmWarning: IProgress not found' – harmless.",
                ],
            },
            {
                "task": "Cloud agent, no tools",
                "task_note": "Step 2",
                "did": [
                    "Built a `CodeAgent` with `InferenceClientModel` (`meta-llama/Llama-3.3-70B-Instruct`) and no tools "
                    "and asked it to add up 1 to 50.",
                    "**2 cycles:** step 1 used the formula n × (first + last) / 2 and printed 1275.0 (2.22 s), step 2 "
                    "called `final_answer(1275.0)` (1.63 s). 4,262 input tokens in total.",
                ],
                "time": "0.5 h",
                "learning": [
                    "A CodeAgent answers by writing Python – smolagents runs the code on my laptop and shows the "
                    "model what it printed. Even with no tools it can still do maths in code.",
                ],
                "problems": [],
            },
            {
                "task": "Web search + two-step task",
                "task_note": "Step 3, `DuckDuckGoSearchTool`",
                "did": [
                    "Added `DuckDuckGoSearchTool()` and asked: search for Melbourne's population, then work out 15%.",
                    "**3 cycles, about 6 s:** step 1 `web_search(...)` (2.83 s), step 2 took 5,300,000 × 0.15 = "
                    "795,000 (1.74 s), step 3 `final_answer(795000)` (1.43 s).",
                    "Watched the loop: Thought → the code it wrote ('Executing parsed code') → Observation ('Execution "
                    "logs', what the code printed) → next step.",
                ],
                "time": "0.5 h",
                "learning": [
                    "The Observation is how the model 'sees' the web – it reads the printed search results and picks "
                    "a number from them in the next step.",
                    "It stops when its code calls `final_answer(...)`.",
                ],
                "problems": [
                    "The search results didn't agree (4.93 million, 'over 5.3 million', 5.32 million metro, 177,000 "
                    "for the City of Melbourne). The agent just picked 5.3 million without saying which source it "
                    "used.",
                ],
            },
            {
                "task": "Memory",
                "task_note": "Step 4, `agent.memory.steps`",
                "did": [
                    "Printed `agent.memory.steps`: one `TaskStep` (my question) and one `ActionStep` per cycle.",
                    "Each ActionStep keeps the step number, the timing (start, end, duration), all the messages sent "
                    "to the model (including the long system prompt), the model's output, the code, what it printed "
                    "and the token usage – all automatic.",
                ],
                "time": "0.5 h",
                "learning": [
                    "The agent's memory is just this list of steps, sent to the model again every time – so the input "
                    "gets bigger each step (about 2,074 → 2,995 → 3,157 tokens per step).",
                ],
                "problems": [],
            },
            {
                "task": "Local model",
                "task_note": "Step 5, `TransformersModel`",
                "did": [
                    "Swapped the model line for `TransformersModel(model_id=\"Qwen/Qwen2.5-1.5B-Instruct\")` and ran "
                    "the same Melbourne task.",
                    "Step 1 searched fine but took **105 s**. Steps 2–15 were all **'Error in code parsing'** "
                    "(188–362 s each) and I stopped it at step 16 – about **73 minutes**, no answer (Fig 2.1).",
                ],
                "time": "1.5 h",
                "learning": [
                    "A 1.5B model can't follow the strict format: it wrote its code as a markdown block (between "
                    "three back-quotes) instead of inside `<code>…</code>` tags, so smolagents couldn't run any of it – even though the error message told "
                    "it exactly what to do.",
                    "Its first attempt (5,350,705 × 0.15) was right, just in the wrong format. After that it kept "
                    "'answering' with a variable that never existed. The default `max_steps` is 20, so a lower limit "
                    "would have saved me an hour.",
                ],
                "problems": [
                    "Very slow on my laptop's CPU (minutes per step) and it never finished.",
                    "'Warning: You are sending unauthenticated requests to the HF Hub' – the token was only given to "
                    "the cloud model; harmless.",
                ],
            },
            {
                "task": "Cloud vs local",
                "task_note": "Step 6, `run_and_time`",
                "did": [
                    "Used the sheet's code: two agents that only differ in the model line, quiet logs "
                    "(`LogLevel.ERROR`) and `run_and_time`, with 'What is the current weather in Melbourne?'.",
                    "The cloud run failed straight away: **402 Payment Required** – 'You have depleted your monthly "
                    "included credits'. Because it crashed first, the local run never started.",
                ],
                "time": "0.5 h",
                "learning": [
                    "The free cloud tier has a monthly limit – local is slow but never runs out.",
                ],
                "problems": [
                    "No timing comparison for the weather question. Next time I'd put each run in a `try` so the "
                    "local one still runs, and do the comparison on the Melbourne task instead (table below).",
                ],
            },
            {
                "task": "GradioUI chat",
                "task_note": "Step 7",
                "did": [
                    "Wrapped the agent with the search tool in `GradioUI(agent).launch()` – the chat opened at "
                    "http://127.0.0.1:7860 and I typed 'hello'.",
                ],
                "time": "0.5 h",
                "learning": [
                    "GradioUI shows the agent's steps in the chat, not just the final answer.",
                ],
                "problems": [
                    "It answered with '400 – model does not exist', because I typed the model name as "
                    "`meta-llama-3.3-70B-Instruct` instead of `meta-llama/Llama-3.3-70B-Instruct` (and my credits "
                    "were used up anyway).",
                    "`launch()` keeps the cell running, so I had to stop it (KeyboardInterrupt) to use the notebook "
                    "again.",
                ],
            },
            {
                "task": "Class notes",
                "task_note": "Agent architecture & design patterns",
                "did": [
                    "What makes an AI system 'agentic': it works towards a goal by reasoning, planning, memory, using "
                    "tools and repeating actions (observe → think → plan → act → repeat).",
                    "Core parts: the LLM (the brain), memory, a planner, a tool executor, the environment and "
                    "reflection. Memory types: working, short-term, long-term and procedural.",
                    "Three design patterns – tool use, reflection (generate → critique → refine) and planning – and "
                    "autonomy levels L0 (prompt-based) to L5 (full autonomy).",
                ],
                "time": "1 h",
                "learning": [
                    "The context window isn't memory – it's temporary. Real memory is stored, searched and reused, "
                    "and finding the right thing matters more than storing more.",
                    "Today's agent was a mix of tool use and planning; the error messages fed back to the model are "
                    "a simple kind of reflection.",
                ],
                "problems": [],
            },
            {
                "task": "Checkpoint questions",
                "task_note": "+ deliverable",
                "did": ["Answered the 4 checkpoint questions and made the cloud vs local table (below)."],
                "time": "0.5 h",
                "learning": ["A framework saves a lot of code, but you still have to read the steps to trust the "
                             "answer."],
                "problems": [],
            },
        ],
        "total_time": "6 h",
        "total_note": "+ ~20 min for screenshots",
        "screenshots_intro": "Figure 2.1 is made from the step times my notebook printed. The yellow boxes are "
                             "screenshots I still need to add (take them from `Lab2_completed.ipynb` – the copy "
                             "without the token).",
        "figures": [
            {"path": "Lab 2/figures/2_1_step_times.png", "width": 6.2,
             "caption": "seconds per step for the same task – cloud (3 steps, done) vs local (16 steps, stopped)"},
        ],
        "screenshots": [
            {"id": "2.1", "title": "Hugging Face – my access token",
             "what": "huggingface.co → Settings → Access Tokens with your (new) token in the list – the value is "
                     "hidden. Not the pop-up that shows the full token.",
             "file": "Lab 2/screenshots/2.1_hf_token.png"},
            {"id": "2.2", "title": "Notebook – cloud agent, no tools",
             "what": "the sum of 1 to 50 run: the 'New run' box, Step 1 (the formula code + 1275.0), Step 2 "
                     "(final_answer) and the 1275.0 printed at the end.",
             "file": "Lab 2/screenshots/2.2_no_tools.png"},
            {"id": "2.3", "title": "Notebook – web search, 3 cycles",
             "what": "the Melbourne run: Step 1 with `web_search(...)` + the start of its search results, then Steps "
                     "2 and 3 with 795000. Two shots are fine: `2.3a_…` + `2.3b_…`.",
             "file": "Lab 2/screenshots/2.3_web_search.png"},
            {"id": "2.4", "title": "Notebook – agent.memory.steps",
             "what": "the memory cell: the `TaskStep(...)` line and the start of the `ActionStep(step_number=1, "
                     "timing=…` lines.",
             "file": "Lab 2/screenshots/2.4_memory.png"},
            {"id": "2.5", "title": "Notebook – local model stuck",
             "what": "the local run: Step 1 (105 s) and a couple of the 'Error in code parsing' steps with their "
                     "durations. Two shots are fine: `2.5a_…` + `2.5b_…`.",
             "file": "Lab 2/screenshots/2.5_local_model.png"},
            {"id": "2.6", "title": "Notebook – cloud vs local, 402 error",
             "what": "the `run_and_time` cell and its '402 Payment Required … depleted your monthly included "
                     "credits' error.",
             "file": "Lab 2/screenshots/2.6_cloud_vs_local_402.png"},
            {"id": "2.7", "title": "GradioUI chat",
             "what": "the GradioUI page at http://127.0.0.1:7860 with your message (and the reply or the error).",
             "file": "Lab 2/screenshots/2.7_gradio_ui.png"},
            {"id": "2.8", "title": "Notebook – checkpoint answers",
             "what": "the 'Checkpoint questions' cell at the end of the notebook.",
             "file": "Lab 2/screenshots/2.8_checkpoint.png"},
        ],
        "sections": [
            {
                "heading": "Deliverable – same agent, cloud vs local",
                "paragraphs": ["Same `CodeAgent`, same `DuckDuckGoSearchTool`, same task ('search for the current "
                               "population of Melbourne, then calculate 15%') – only the model line changed. "
                               "Numbers are from my notebook's step logs."],
                "table": {"header": ["", CLOUD, LOCAL], "rows": COMPARISON, "widths": [2165, 3400, 3400]},
            },
            {
                "heading": "Checkpoint questions",
                "qa": CHECKPOINT,
            },
        ],
    }
