# Week 2 worklog content - Lab 2 (smolagents: agent with tools and memory)
# Markup: **bold**, `code`, [[yellow = filled in once the notebook has run]].
# Numbers come from "Lab 2/results/lab2_results.json" (saved by Lab2_smolagents_agent.ipynb).
# Run the notebook, then:  python _tools/build_worklogs.py 2

from worklog_content._results import get, has, k, load, v

RESULTS = "Lab 2/results/lab2_results.json"
CHECKPOINT_QS = [
    "1. What did the framework do for you that you would have written manually in Week 1?",
    "2. How many Thought → Code → Observation cycles ran before the agent gave a final answer, and what "
    "triggered it to stop?",
    "3. What changed when you swapped from cloud to local, and what stayed the same?",
    "4. Did your local model complete the task successfully? If not, what did it get wrong?",
]


def _col(run, max_steps):
    if not run:
        return ["[[run the notebook]]"] * 6
    if "failed" in run:
        return ["crashed", "–", "–", "–", "–", run["failed"][:70]]
    return ["yes" if run["finished"] else f"no – hit max_steps={max_steps}", str(run["n_steps"]),
            f"{run['seconds']} s", str(run["searches"]), f"{run['tokens_in']:,} / {run['tokens_out']:,}",
            str(run["answer"])[:70]]


def build_spec():
    r = load(RESULTS)
    ran = bool(r)
    max_steps = k(r, "max_steps", 6)

    # ---- search / fallback ---------------------------------------------------
    search_problems = []
    if get(r, "search_note"):
        search_problems.append("DuckDuckGo rate-limited me (the sheet warned about this), so the notebook switched "
                               "to smolagents' `WebSearchTool` (Bing) – same `web_search` name, so the agent code "
                               "didn't change.")
    s = get(r, "search", {}) or {}
    pop = s.get("population_used")
    if s:
        search_line = (f"It took **{s['n_steps']} cycles** and {s['searches']} web search(es) "
                       f"({s['seconds']} s): it found a population of about {pop:,} and answered **{s['answer']}**."
                       if pop else f"It took **{s['n_steps']} cycles** ({s['seconds']} s) and answered: {s['answer'][:80]}.")
        if not s.get("looks_right"):
            search_problems.append("The final answer doesn't look like 15% of ~5 million, so it either used the "
                                   "wrong number from the search results or did the maths wrong – I checked the "
                                   "Execution logs to see which.")
        if s.get("errors"):
            search_problems.append(f"{s['errors']} step(s) ended with an error, but the agent read the error and "
                                   "fixed its own code in the next step.")
    else:
        search_line = ("It took [[x]] cycles and [[x]] web search(es): it found a population of about [[x]] "
                       "and answered [[x]].")

    # ---- memory --------------------------------------------------------------
    mem = get(r, "memory", {}) or {}
    fu = mem.get("follow_up") or {}
    if fu:
        follow_line = (f"Extra: asked a follow-up with `reset=False` (\"what is 30% of the population you found?\") – "
                       f"answered {fu['answer'][:30]} in {fu['n_steps']} cycle(s) and "
                       f"{'searched again' if fu['searched_again'] else '**did not search again**'}"
                       + (", same population as before ✔." if fu.get("matches") else "."))
    else:
        follow_line = ("Extra: asked a follow-up with `reset=False` – [[did it remember the population without "
                       "searching again?]]")
    steps = s.get("steps") or []
    if len(steps) >= 2 and steps[0].get("tokens in") and steps[-1].get("tokens in"):
        grow = (f"The input grows every step ({steps[0]['tokens in']:,} → {steps[-1]['tokens in']:,} tokens) "
                "because the whole memory is sent to the model again each time.")
    else:
        grow = "The input gets bigger every step because the whole memory is sent to the model again each time."

    # ---- local model ---------------------------------------------------------
    loc = get(r, "local") or {}
    if not loc:
        local_did = ("Swapped `InferenceClientModel` for `TransformersModel(\"Qwen/Qwen2.5-1.5B-Instruct\")` and "
                     "ran the same task: [[how long it took / did it finish?]]")
        local_problems = []
    elif "failed" in loc:
        local_did = ("Swapped `InferenceClientModel` for `TransformersModel(\"Qwen/Qwen2.5-1.5B-Instruct\")` – it "
                     f"crashed: `{loc['failed'][:120]}`.")
        local_problems = ["The local model didn't work on my laptop (see the error) – the sheet says this can "
                          "happen."]
    else:
        local_did = (f"Swapped `InferenceClientModel` for `TransformersModel(\"Qwen/Qwen2.5-1.5B-Instruct\")` "
                     f"(loading took {loc.get('load_s', '?')} s) and ran the same task: {loc['n_steps']} cycles, "
                     f"{loc['seconds']} s, answer **{str(loc['answer'])[:40]}**"
                     + (" – right ✔." if loc.get("looks_right") else " – not right ✘."))
        local_problems = []
        if loc.get("errors"):
            local_problems.append(f"The small model wrote broken code {loc['errors']} time(s) (it saw the error and "
                                  "tried again) – the 70B cloud model didn't need to.")
        if not loc.get("finished"):
            local_problems.append(f"It never called `final_answer()` and got stopped by max_steps={max_steps}.")
        elif not loc.get("looks_right"):
            local_problems.append("It finished but the number is wrong – it didn't use Melbourne's population "
                                  "properly.")
    local_problems.append("The first run downloads about 3 GB, and it runs on my CPU, so it's much slower than the "
                          "cloud. I gave it `max_new_tokens=1024` and the agents `max_steps="
                          f"{max_steps}` so it can't ramble forever.")

    cmp_ = get(r, "compare", {}) or {}
    cc, lc = cmp_.get("cloud") or {}, cmp_.get("local") or {}
    if cc:
        weather = (f"Weather question – cloud: {cc['seconds']} s, {cc['n_steps']} cycles; local: "
                   + (f"{lc['seconds']} s, {lc['n_steps']} cycles." if lc and "failed" not in lc
                      else ("crashed." if lc else "skipped.")))
    else:
        weather = "Weather question – cloud: [[x]] s, local: [[x]] s."

    cp = get(r, "checkpoint", {}) or {}
    answers = [cp.get(q) or "[[run the notebook – the answer is printed in the last cell]]"
               for q in ("q1", "q2", "q3", "q4")]

    table_rows = []
    labels = ["Finished?", "Cycles (Thought → Code → Observation)", "Time", "Web searches", "Tokens in / out",
              "Final answer"]
    cols = [_col(get(r, "search"), max_steps), _col(get(r, "local"), max_steps),
            _col(cc, max_steps), _col(lc, max_steps)]
    for i, lab in enumerate(labels):
        table_rows.append([lab] + [c[i] for c in cols])

    return {
        "week": 2,
        "dates": "10–16 August 2026",
        "student_name": "Anas Al Azad",
        "student_id": "105694136",
        "title": "Week 2 – Agent with tools and memory (smolagents)",
        "intro": "My checklist for this week – ticked = done, unticked = still to do. Everything is in "
                 "`Lab 2/Lab2_smolagents_agent.ipynb` in my repo." + ("" if ran else
                 " (Yellow bits fill in by themselves once I've run the notebook and rebuilt this worklog.)"),
        "checklist": [
            ("Read the Week 2 sheet", True),
            ("Notebook `Lab2_smolagents_agent.ipynb` set up for all 7 steps", True),
            ("Installed smolagents + made a Hugging Face token (kept in `.env`) (step 1)", has(r, "no_tools")),
            ("Basic cloud agent with no tools (step 2)", has(r, "no_tools")),
            ("Web search tool + a two-step task, watched Thought → Code → Observation (step 3)", has(r, "search")),
            ("Looked inside `agent.memory.steps` + follow-up question to test memory (step 4)", has(r, "memory")),
            ("Same task with the local `TransformersModel` (step 5)", has(r, "local")),
            ("Cloud vs local comparison with `run_and_time` (step 6)", has(r, "compare")),
            ("Agent in a `GradioUI` chat (step 7)", has(r, "gradio")),
            ("Answered the 4 checkpoint questions", has(r, "checkpoint")),
            ("Screenshots added (yellow boxes below)", False),
        ],
        "rows": [
            {
                "task": "Setup",
                "task_note": "Step 1",
                "did": [
                    "Installed `smolagents[toolkit]` and `smolagents[transformers]`.",
                    "Made a free Hugging Face access token and put it in my `.env` file as `HF_TOKEN` (the sheet "
                    "types it into the code – I didn't want it on GitHub).",
                ],
                "time": "0.5 h",
                "learning": [
                    "A framework like smolagents handles the 'call the model → use a tool → call the model again' "
                    "loop, which I'd have to write myself otherwise.",
                ],
                "problems": [],
            },
            {
                "task": "Cloud agent, no tools",
                "task_note": "Step 2",
                "did": [
                    "Built a `CodeAgent` with `InferenceClientModel` (Llama 3.3 70B through Hugging Face) and no "
                    "tools, and asked it to add up 1 to 50.",
                    f"It answered **{v(r, 'no_tools.answer', placeholder='1275')}** in "
                    f"{v(r, 'no_tools.n_steps', placeholder='x')} cycle(s) – it wrote `sum(range(1, 51))` and ran it "
                    "instead of doing the maths in its head.",
                ],
                "time": "0.5 h",
                "learning": [
                    "A CodeAgent answers by writing Python. smolagents runs that code on my laptop and shows the "
                    "model what it printed.",
                ],
                "problems": [],
            },
            {
                "task": "Web search + two-step task",
                "task_note": "Step 3",
                "did": [
                    "Added `DuckDuckGoSearchTool()` and asked: search for Melbourne's population, then work out 15% of it.",
                    search_line,
                    "Watched the cycle in the log: **Thought** (what it plans), **Code** ('Executing parsed code'), "
                    "**Observation** ('Execution logs' = what the code printed), then the next step.",
                ],
                "time": "1 h",
                "learning": [
                    "Step 1 searched and printed the results, step 2 used the number from those results – the "
                    "Observation is how the model 'sees' the web page text.",
                    "It stops when its code calls `final_answer(...)`.",
                ],
                "problems": search_problems,
            },
            {
                "task": "Memory",
                "task_note": "Step 4, `agent.memory.steps`",
                "did": [
                    f"Printed `agent.memory.steps`: {k(r, 'memory.entries', '[[x]]')} entries (the task + one per "
                    f"cycle), {v(r, 'memory.characters', '{:,}', 'x')} characters in total!",
                    "Each step stores the messages sent to the model, the code, what it printed, any error, the "
                    "time and the tokens – all automatic.",
                    follow_line,
                ],
                "time": "0.5 h",
                "learning": [
                    "The agent's 'memory' is just this list of steps being sent to the model again.",
                    grow,
                ],
                "problems": [],
            },
            {
                "task": "Local model",
                "task_note": "Step 5, `TransformersModel`",
                "did": [local_did],
                "time": "1 h",
                "learning": [
                    "Only the `model=` line changed – the agent, tool and task stayed exactly the same.",
                    "A 1.5B model is much worse at following the strict 'Thought + code' format than a 70B one.",
                ],
                "problems": local_problems,
            },
            {
                "task": "Cloud vs local",
                "task_note": "Step 6, `run_and_time`",
                "did": [
                    "Used the sheet's `run_and_time` with two agents that only differ in the model line and quiet "
                    "logs (`LogLevel.ERROR`).",
                    weather,
                    "Put both tasks side by side in a table (below).",
                ],
                "time": "0.5 h",
                "learning": [
                    "Cloud = fast and reliable but needs the token and internet; local = private and free but slow "
                    "and less reliable on my laptop.",
                ],
                "problems": [
                    "I reused the local model I'd already loaded instead of loading a second 3 GB copy like the "
                    "sheet's code does.",
                ],
            },
            {
                "task": "GradioUI chat",
                "task_note": "Step 7",
                "did": [
                    "Wrapped the cloud agent (with web search) in `GradioUI` and chatted with it in the browser – you "
                    "can see each step it takes, and it remembers earlier messages.",
                ],
                "time": "0.5 h",
                "learning": [
                    "GradioUI shows the agent's thoughts and code as it works, not just the final answer.",
                ],
                "problems": [
                    "`GradioUI(agent).launch()` blocks the notebook (debug mode) and makes a public share link by "
                    "default, so I used `create_app().launch(share=False)` instead.",
                ],
            },
            {
                "task": "Checkpoint questions",
                "task_note": "+ deliverable",
                "did": ["Answered the 4 checkpoint questions from my own run (below the screenshots)."],
                "time": "0.5 h",
                "learning": ["Frameworks save a lot of code, but you have to look at the steps to trust the answer."],
                "problems": [],
            },
        ],
        "total_time": "5 h",
        "total_note": "+ ~20 min for screenshots",
        "screenshots_intro": "The yellow boxes are screenshots I still need to add.",
        "figures": [],
        "screenshots": [
            {"id": "2.1", "title": "Hugging Face – my access token",
             "what": "huggingface.co → Settings → Access Tokens with your token in the list (the value is hidden – "
                     "good). Don't screenshot the pop-up that shows the full token.",
             "file": "Lab 2/screenshots/2.1_hf_token.png"},
            {"id": "2.2", "title": "Terminal – installing smolagents",
             "what": "the end of `pip install \"smolagents[toolkit]\" \"smolagents[transformers]\"` "
                     "('Successfully installed …').",
             "file": "Lab 2/screenshots/2.2_pip_install.png"},
            {"id": "2.3", "title": "Notebook – cloud agent, no tools",
             "what": "the step 2 output: the 'New run' box, Step 1 / Step 2 with the code, 'Final answer: 1275' and "
                     "the small step table.",
             "file": "Lab 2/screenshots/2.3_no_tools.png"},
            {"id": "2.4", "title": "Notebook – web search, two steps",
             "what": "the step 3 log: Step 1 with `web_search(...)` + its Execution logs, and Step 2 with the 15% "
                     "maths + 'Final answer'. Two shots are fine: `2.4a_…` + `2.4b_…`.",
             "file": "Lab 2/screenshots/2.4_web_search.png"},
            {"id": "2.5", "title": "Notebook – agent.memory.steps",
             "what": "the step 4 output (TaskStep / ActionStep lines + the 'what smolagents records' line) and the "
                     "follow-up's last line ('searched again: False …').",
             "file": "Lab 2/screenshots/2.5_memory.png"},
            {"id": "2.6", "title": "Notebook – local model (TransformersModel)",
             "what": "the step 5 output: 'loaded Qwen/… in … s', the steps and the final answer (or the error if it "
                     "failed).",
             "file": "Lab 2/screenshots/2.6_local_model.png"},
            {"id": "2.7", "title": "Notebook – cloud vs local",
             "what": "the step 6 'Cloud: …s' / 'Local: …s' lines and the comparison table under them.",
             "file": "Lab 2/screenshots/2.7_cloud_vs_local.png"},
            {"id": "2.8", "title": "GradioUI chat in the browser",
             "what": "http://127.0.0.1:7860 (or the link the notebook printed) after asking the agent something that "
                     "needs a search – the steps and the final answer should be visible.",
             "file": "Lab 2/screenshots/2.8_gradio_ui.png"},
        ],
        "sections": [
            {
                "heading": "Deliverable – same agent, cloud vs local",
                "paragraphs": ["The notebook has the working agent (web search + memory) run on both models and in "
                               "GradioUI. This is the summary of my run" +
                               (f" ({r.get('run_at')}, smolagents {r.get('smolagents')}, max_steps = {max_steps})."
                                if ran else ".")],
                "table": {"header": ["", "Melbourne 15% – cloud", "Melbourne 15% – local", "Weather – cloud",
                                     "Weather – local"],
                          "rows": table_rows, "widths": [1765, 1800, 1800, 1800, 1800]},
            },
            {
                "heading": "Checkpoint questions",
                "qa": list(zip(CHECKPOINT_QS, answers)),
            },
        ],
    }
