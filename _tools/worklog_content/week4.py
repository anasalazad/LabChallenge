# Week 4 worklog content - Lab 4 (Microsoft AutoGen multi-agent conversation app)
# Markup: **bold**, `code`, [[yellow = filled in once the scripts have run]].
# Numbers come from "Lab 4/results/lab4_results.json" (saved by run_examples.py and groupchat_demo.py).
#     cd "Lab 4/Multiagent";  python run_examples.py;  python groupchat_demo.py
#     python _tools/build_worklogs.py 4

from worklog_content._results import fig, get, load

RESULTS = "Lab 4/results/lab4_results.json"
SHORT = ["sum of two numbers", "'production' follow-up", "stock price chart", "show file"]

FIXES = [
    ["`CONFIG_LIST.json`", "Only a model name + key, no `base_url`, so AutoGen (which talks the OpenAI format) "
     "sends the requests to api.openai.com – a Gemini key gets rejected there.",
     "Added Gemini's OpenAI-compatible address `https://generativelanguage.googleapis.com/v1beta/openai/`."],
    ["`agent.py`", "The key would have to be typed into `CONFIG_LIST.json`, which is in my GitHub repo.",
     "Kept the \"Your API Key\" placeholder; `agent.py` swaps it for `GEMINI_API_KEY` from my `.env`."],
    ["`app.py`", "The avatar pictures `../images/human.png` and `../images/autogen.png` don't exist → broken "
     "image icons in the chat.", "Added the two pictures in `Lab 4/images/` (no code change)."],
    ["`chat.py`", "`chat_respond` put every message into the chat history itself AND returned \"\", so Gradio's "
     "ChatInterface added my message a second time at the bottom with an empty reply bubble.",
     "It now returns the whole agent conversation as one reply (with **assistant** / **userproxy** labels)."],
    ["`chat.py`", "The timeout and error branches returned half a message pair, and 'no API key' returned a "
     "1-item list – the chat window can't show either.", "They return a normal text reply now."],
    ["`chat.py`", "`chat_respond` asks for 4 extra values (model, keys…) the window never sends – Gradio just fills "
     "them with None.", "Made them optional so it's clear they're not used."],
    ["`chat.py`", "After a `show file:` reply, the file itself (not text) went into the history that is sent to "
     "Gemini with the next question.", "The history turns a file into the text '[a file was shown in the chat]'."],
]

QA = [
    ("How do the two agents work together?",
     "The **assistant** is the one that talks to Gemini – it writes a plan and Python code. The **userproxy** stands "
     "in for me: it never asks me anything (`human_input_mode=\"NEVER\"`), it just runs the code in the `coding/` "
     "folder and sends back 'exitcode: 0 … Code output: …' (or the error). The assistant reads that and either fixes "
     "the code or finishes. That back-and-forth is the 'multi-agent conversation'."),
    ("What makes the conversation stop?",
     "`_is_termination_msg` in `agent.py`: the userproxy stops replying as soon as the assistant sends a message "
     "with no Python code block in it (usually the one ending in TERMINATE). There's also a limit of 5 automatic "
     "replies each, and `chat.py` kills the whole thing after 60 seconds."),
    ("How does it remember the earlier messages?",
     "Each new question starts a fresh AutoGen chat, but `chat.py` turns the Gradio chat history into OpenAI-style "
     "messages and adds them to the assistant's system messages first – that's why 'what if the production of two "
     "numbers?' knows we were talking about the sum function."),
    ("What's risky about this set-up?",
     "It runs code an AI wrote straight on my laptop, without asking me and without Docker "
     "(`use_docker: False`). A bad answer could delete or overwrite files. Safer options: `use_docker=True`, or "
     "`human_input_mode=\"ALWAYS\"` so I approve each run."),
    ("How is this different from smolagents in Week 2?",
     "In smolagents one agent writes code and the framework runs it. In AutoGen the code runner is an agent too, so "
     "it's a conversation between agents – and it's easy to add more of them, which is what I did with the critic."),
]


def build_spec():
    r = load(RESULTS)
    ex = get(r, "examples") or {}
    gc = get(r, "groupchat") or {}
    runs = ex.get("runs") or []
    model = ex.get("model") or gc.get("model") or "gemini-3.5-flash-lite"

    # ---- example results -------------------------------------------------------------
    ex_lines, ex_problems, table_rows = [], [], []
    if runs:
        for name, run in zip(SHORT, runs):
            if run["reply_is_file"]:
                ex_lines.append(f"**{name}**: showed `stock_price.png` straight in the chat (no model call).")
                table_rows.append([name, "–", "–", "–", "–", "showed the chart" if ex.get("stock_png") else "file not found"])
                continue
            status = ("timed out" if run["timeout"] else "error" if run["error"] else
                      "finished (TERMINATE)" if run["ended_with_terminate"] else "stopped")
            ex_lines.append(f"**{name}**: {run['seconds']} s, {run['messages']} messages, code run "
                            f"{run['code_runs']} time(s) (exit codes {run['exitcodes'] or '–'}), {status}.")
            table_rows.append([name, f"{run['seconds']} s", str(run["messages"]), str(run["code_runs"]),
                               ", ".join(map(str, run["exitcodes"])) or "–", status])
            if any(c != 0 for c in run["exitcodes"]):
                fixed = run["exitcodes"] and run["exitcodes"][-1] == 0
                ex_problems.append(f"'{name}': the first code failed (exit code {run['exitcodes'][0]})"
                                   + (" – the assistant read the error and fixed it, then it worked." if fixed else
                                      " and it never got it working."))
            if run["shell_blocks"] and not run["ended_with_terminate"]:
                ex_problems.append(f"'{name}': the assistant answered with a shell command (e.g. `pip install`) "
                                   "instead of Python. The stop rule only looks for Python code blocks, so the chat "
                                   "ended before anything ran.")
            if run["timeout"]:
                ex_problems.append(f"'{name}' hit the 60-second time limit in `chat.py`.")
        if ex.get("stock_png"):
            stock_line = "The agents made `coding/stock_price.png` (Fig 4.1)."
        else:
            stock_line = "No `stock_price.png` was made – [[why: see the transcript]]."
            ex_problems.append("The stock chart wasn't saved – see `results/lab4_transcripts.md` for what went wrong.")
    else:
        ex_lines = ["[[for each example: how long it took, how many messages, how many times code ran, how it "
                    "ended]]"]
        stock_line = "[[did the agents save coding/stock_price.png?]]"
        table_rows = [[n, "[[ ]]", "[[ ]]", "[[ ]]", "[[ ]]", "[[ ]]"] for n in SHORT]

    if runs and len(runs) > 1 and runs[1]["exitcodes"] and runs[1]["exitcodes"][-1] == 0:
        followup = ("The 'production' follow-up worked without repeating what I meant – `chat.py` sends the earlier "
                    "chat along as context, so it knew we were talking about two numbers.")
    else:
        followup = ("The follow-up question only makes sense because `chat.py` sends the earlier chat along as "
                    "context.")

    # ---- group chat --------------------------------------------------------------------
    if gc:
        gc_line = (f"Ran it on a palindrome task: {gc['messages']} messages in {gc['seconds']} s "
                   f"({', '.join(f'{k} {v}' for k, v in gc['by_agent'].items())}); the critic "
                   + ("**approved the first version**" if gc["critic_approved_first_time"] else
                      "**asked for changes first**")
                   + f", exit codes {gc['exitcodes'] or '–'}"
                   + (", ended with TERMINATE." if gc["ended_with_terminate"] else ", stopped at the round limit."))
        gc_critic = gc.get("critic_first", "")[:160].replace("\n", " ")
    else:
        gc_line = "Ran it on a palindrome task: [[messages, who said what, did the critic approve, exit codes]]"
        gc_critic = ""

    return {
        "week": 4,
        "dates": "24–30 August 2026",
        "student_name": "Anas Al Azad",
        "student_id": "105694136",
        "title": "Week 4 – Multi-agent conversation with Microsoft AutoGen",
        "intro": "My checklist for this week – ticked = done, unticked = still to do. The app is in "
                 "`Lab 4/Multiagent/` in my repo." + ("" if r else
                 " (Yellow bits fill in by themselves once I've run the scripts and rebuilt this worklog.)"),
        "checklist": [
            ("Read through the tutor's AutoGen app (`agent.py`, `chat.py`, `app.py`, `utils.py`)", True),
            ("Fixed the bugs that stopped it working with Gemini + the display bugs (table below)", True),
            ("Python 3.12 virtual environment + `pip install -r requirements.txt` (+ `yfinance`)", bool(runs)),
            ("Gemini key in `.env` (not in `CONFIG_LIST.json`)", bool(runs)),
            ("Ran `python app.py` and tried all 4 example prompts in the browser", False),
            ("`run_examples.py` – same 4 prompts without the browser, results + transcripts saved", bool(runs)),
            ("Extension: coder + critic + executor group chat (`groupchat_demo.py`)", bool(gc)),
            ("Answered my own questions about how it works (below)", True),
            ("Screenshots added (yellow boxes below)", False),
        ],
        "rows": [
            {
                "task": "Setting up",
                "task_note": "Python 3.12, requirements.txt",
                "did": [
                    "Made a separate virtual environment with **Python 3.12** (`.venv-autogen`) and ran "
                    "`pip install -r requirements.txt yfinance` (yfinance is for the stock-price example).",
                    "Put my Gemini key in `.env` and pointed `CONFIG_LIST.json` at Gemini (`" + model + "`).",
                ],
                "time": "0.5 h",
                "learning": [
                    "Old libraries are pinned to old versions for a reason – `pyautogen==0.2.28` only supports "
                    "Python 3.8–3.12, so it needs its own environment.",
                ],
                "problems": [
                    "`pip install pyautogen==0.2.28` fails on Python 3.13 or newer ('No matching distribution') – "
                    "that's why this lab gets a Python 3.12 environment of its own.",
                ],
            },
            {
                "task": "Reading the code",
                "task_note": "agent.py, chat.py, app.py, utils.py",
                "did": [
                    "`agent.py`: two agents – **assistant** (writes code with Gemini) and **userproxy** (runs the "
                    "code in `coding/` with no human input); the chat stops when the assistant's message has no "
                    "Python code in it; max 5 automatic replies each.",
                    "`chat.py`: turns the Gradio chat history into messages for the assistant, runs the agent chat in "
                    "a thread and kills it after 60 s; `show file:` shows a file from `coding/`.",
                    "`app.py`: the Gradio page (ChatInterface + 4 example prompts) on port 7868.",
                ],
                "time": "1 h",
                "learning": [
                    "Multi-agent = agents with different jobs talking to each other: one writes, one runs and reports "
                    "back, and the loop goes on until the stop rule fires.",
                    "AutoGen 0.2 caches model replies in a `.cache` folder, so asking the exact same thing twice "
                    "comes back instantly from the cache.",
                ],
                "problems": [],
            },
            {
                "task": "Fixing the app",
                "task_note": "my changes are marked (my fix)",
                "did": [
                    "Gemini: added the OpenAI-compatible `base_url` to `CONFIG_LIST.json` and made `agent.py` read "
                    "the key from `.env`.",
                    "Added the two missing avatar pictures, and changed `chat.py` so each answer is one reply "
                    "(no repeated message + empty bubble) and errors/timeouts show up as normal messages.",
                    "Full list in the table under the screenshots.",
                ],
                "time": "1.5 h",
                "learning": [
                    "Gradio's ChatInterface adds [my message, your reply] to the chat by itself – the function should "
                    "just return the reply.",
                    "Many providers (Gemini included) offer an 'OpenAI-compatible' address, so tools built for OpenAI "
                    "can use them by changing the URL.",
                ],
                "problems": [
                    "Out of the box the requests would go to OpenAI with a Gemini key (rejected), the avatars were "
                    "broken and every answer repeated my message with an empty bubble – all fixed.",
                ],
            },
            {
                "task": "Running the examples",
                "task_note": "`app.py` + `run_examples.py`",
                "did": [
                    "Ran `python app.py`, opened http://127.0.0.1:7868 and tried the 4 example prompts.",
                    "Wrote `run_examples.py` – sends the same 4 prompts through the same `chat_respond` function "
                    "without the browser and saves the numbers + full transcripts (`results/lab4_transcripts.md`).",
                ] + ex_lines + [stock_line],
                "time": "1 h",
                "learning": [
                    followup,
                    "Everything the assistant wrote and the userproxy ran is saved in `coding/` – the code really "
                    "ran on my laptop.",
                ],
                "problems": ex_problems,
            },
            {
                "task": "Extension – 3 agents",
                "task_note": "`groupchat_demo.py`",
                "did": [
                    "Added a third agent: a **critic** that reviews the code before the executor runs it. Used "
                    "AutoGen's `GroupChat` with a fixed speaking order (coder → critic → executor).",
                    gc_line,
                ] + ([f"The critic said: \"{gc_critic}…\""] if gc_critic else []),
                "time": "1 h",
                "learning": [
                    "More agents = more model calls (slower, more tokens) but you get a second opinion before code runs.",
                    "Round robin is cheap and predictable; `speaker_selection_method=\"auto\"` would ask the model "
                    "who should talk next every turn.",
                ],
                "problems": [
                    "Group chat messages carry a 'name' field that not every OpenAI-compatible API accepts, so I moved "
                    "the speaker's name into the message text instead (a small hook on each agent).",
                ],
            },
        ],
        "total_time": "5 h",
        "total_note": "+ ~20 min for screenshots",
        "screenshots_intro": "Figure 4.1 is the chart the agents made for the third example. The yellow boxes are "
                             "screenshots I still need to add (never with the API key visible).",
        "figures": [
            fig("Lab 4/figures/4_1_stock_price.png",
                "the chart AutoGen's agents made for 'Plot a chart of the last year's stock prices…'", 5.0),
        ],
        "screenshots": [
            {"id": "4.1", "title": "Terminal – Python 3.12 environment + install",
             "what": "the terminal showing `python --version` (3.12.x) inside `.venv-autogen` and the end of "
                     "`pip install -r requirements.txt yfinance` ('Successfully installed …').",
             "file": "Lab 4/screenshots/4.1_venv_install.png"},
            {"id": "4.2", "title": "My fix – CONFIG_LIST.json + agent.py",
             "what": "VS Code with `CONFIG_LIST.json` (the `base_url` line, key still 'Your API Key') and the "
                     "`(my fix)` lines in `agent.py`. Two shots are fine: `4.2a_…` + `4.2b_…`.",
             "file": "Lab 4/screenshots/4.2_config_fix.png"},
            {"id": "4.3", "title": "Terminal – python app.py",
             "what": "the terminal after `python app.py`: 'Running on local URL: http://0.0.0.0:7868'.",
             "file": "Lab 4/screenshots/4.3_app_running.png"},
            {"id": "4.4", "title": "Browser – example 1 (sum of two numbers)",
             "what": "http://127.0.0.1:7868 after clicking the first example: the assistant's code, the "
                     "userproxy's 'exitcode: 0' and the final answer.",
             "file": "Lab 4/screenshots/4.4_example_sum.png"},
            {"id": "4.5", "title": "Browser – example 2 (follow-up)",
             "what": "the reply to 'what if the production of two numbers?' (it should use multiplication).",
             "file": "Lab 4/screenshots/4.5_example_product.png"},
            {"id": "4.6", "title": "Browser – example 3 + 4 (stock chart)",
             "what": "the reply to the stock-price example and then 'show file: stock_price.png' with the chart "
                     "shown in the chat. Two shots are fine: `4.6a_…` + `4.6b_…`.",
             "file": "Lab 4/screenshots/4.6_example_stock_chart.png"},
            {"id": "4.7", "title": "Terminal – run_examples.py",
             "what": "the end of `python run_examples.py`: the '--> … s | … messages | code run …' line of each "
                     "example and 'saved …'.",
             "file": "Lab 4/screenshots/4.7_run_examples.png"},
            {"id": "4.8", "title": "Terminal – groupchat_demo.py (extension)",
             "what": "the output of `python groupchat_demo.py`: 'Next speaker: critic', the critic's APPROVED (or its "
                     "comments), the executor's exit code and the summary line at the end.",
             "file": "Lab 4/screenshots/4.8_groupchat.png"},
        ],
        "sections": [
            {
                "heading": "What I fixed in the tutor's app",
                "paragraphs": ["All changes are marked `(my fix)` in the code."],
                "table": {"header": ["File", "Problem", "My fix"], "rows": FIXES, "widths": [1300, 4165, 3500]},
            },
            {
                "heading": "Results – the 4 example prompts",
                "paragraphs": ["From `run_examples.py`" + (f" ({ex['run_at']}, `{model}`)" if ex else "") +
                               " – same code as the chat window, history passed along."],
                "table": {"header": ["Example", "Time", "Messages", "Code runs", "Exit codes", "How it ended"],
                          "rows": table_rows, "widths": [2165, 1100, 1200, 1200, 1300, 2000]},
            },
            {
                "heading": "Questions I asked myself (no lab sheet this week)",
                "qa": [(f"{i}. {q}", a) for i, (q, a) in enumerate(QA, 1)],
            },
        ],
    }
