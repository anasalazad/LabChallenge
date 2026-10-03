"""
Builds START_HERE_Labs1-4_click_by_click.pdf (repo root): a beginner, click-by-click guide
for Anas to finish Labs 1-4 (Weeks 1-4). Written Mac-first, with Windows notes.

    python _tools/make_guide_labs1_4.py

Needs: pip install reportlab   (re-uses the look of make_beginner_guide.py)
"""
import os
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import KeepTogether, PageBreak, SimpleDocTemplate, Spacer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_beginner_guide import (BODY, BLUE, BLUE_BG, GREEN, GREEN_BG, GREY, GREY_BG, NAVY, P, W,  # noqa: E402
                                 band, box, cmd, key, menu, mono, reset_steps, shot, step, table, tip, warn)

from make_beginner_guide import S as STYLES  # noqa: E402

for _name in ("h2", "h3"):          # never leave a heading alone at the bottom of a page
    STYLES[_name].keepWithNext = 1

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "START_HERE_Labs1-4_click_by_click.pdf")
BRANCH = "claude/optimistic-cray-x20tfr"


def win(text):
    return [Spacer(1, 2), box([P(f"<b>On Windows:</b> {text}", "small")], GREY_BG, colors.HexColor("#AAAAAA")),
            Spacer(1, 3)]


def plain(text):
    return [box([P('<font color="#2E7D32"><b>WHAT THIS WEEK IS ABOUT (in plain English)</b></font>'),
                 Spacer(1, 3), P(text)], GREEN_BG, GREEN), Spacer(1, 6)]


def keys_warning():
    return warn("Your keys go <b>only</b> in the <b>.env</b> file. Never type them into a notebook or a .py file, "
                "never show them in a screenshot, never send them to anyone. If one ever leaks, delete it on the "
                "website and make a new one.", "KEEP YOUR KEYS SECRET")


def finish_week(n, manual_items, note=""):
    """The same routine at the end of every week."""
    items = " ".join(str(i) for i in manual_items)
    reset_steps()
    out = [P(f"Finish your Week {n} worklog", "h2"),
           P("Do these <b>in this order</b> – the first step fills the worklog with your real numbers, and it "
             "only works while the worklog is still untouched.", "small")]
    out.append(step("<b>Close Word</b> if the worklog is open. In <b>Tab 2</b> make sure you're in the "
                    "<b>LabChallenge</b> folder with <b>(.venv)</b> at the start of the line "
                    "(if not: " + mono("cd ~/Documents/LabChallenge") + " then " + mono("source .venv/bin/activate")
                    + ")."))
    out.append(step("Fill the worklog with the numbers from <b>your</b> run:",
                    cmd(f"python _tools/build_worklogs.py {n}"),
                    P(f"It should say <b>week {n}: wrote Lab {n}/Lab{n}_Worklog_Week{n}.docx</b>. The yellow "
                      "placeholders are now your real results.", "small")))
    out.append(step("Put your screenshots in:", cmd(f"python _tools/insert_screenshots.py {n}"),
                    P("It lists what it <b>inserted</b> and what's <b>still missing</b>. Missing? Check the file is in "
                      f"<b>Lab {n} › screenshots</b> and its name starts with the exact number.", "small")))
    out.append(step("Tick the checklist items only you can know about:",
                    cmd(f"python _tools/tick_checklist.py {n} {items}"),
                    P("(Run " + mono(f"python _tools/tick_checklist.py {n}") + " on its own to see all items with "
                      f"their numbers.) {note}", "small")))
    out.append(step(f"Open <b>Lab {n} › Lab{n}_Worklog_Week{n}.docx</b> (double-click in Finder). Read it once – "
                    "it's written as you, so change anything you wouldn't say. Change the <b>TIME SPENT</b> numbers "
                    "to how long it really took you. Save with " + key("Cmd") + " + " + key("S") + "."))
    out.append(step("Make the clean copy for your tutor (no checklist, no notes to yourself):",
                    cmd(f"python _tools/make_handin.py {n}"),
                    P(f"It writes <b>Completed Labs › Lab {n} Completed.docx</b> and warns you if a screenshot or a "
                      "yellow placeholder is still missing.", "small")))
    return out


story = []

# ============================================================= cover
story += [Spacer(1, 1.2 * cm), P("COS30018 Intelligent Systems", "cover_s"), Spacer(1, 4),
          P("Finishing Labs 1 – 4:<br/>a click-by-click guide", "cover_t"), Spacer(1, 8),
          P("Written for Anas – follow it from top to bottom, one week at a time.", "cover_s"), Spacer(1, 16)]
story.append(box([
    P("<b>How this works</b>"), Spacer(1, 4),
    P("All the <b>code</b> for Labs 1–4 is already written and tested, and each week's <b>worklog</b> is already "
      "written for you. What's left needs <b>your</b> accounts and <b>your</b> laptop: make the free API keys, run "
      "the notebooks/scripts (they talk to real AI models, so they can't run without your keys), take the "
      "screenshots, and press one command that fills the worklog with your real numbers."),
    Spacer(1, 6),
    P("The worklogs have <b>yellow placeholders</b> where your results go. You never type numbers in by hand: "
      "the notebooks save their results to a <b>results</b> folder, and " + mono("build_worklogs.py") +
      " copies them into the worklog."),
], BLUE_BG, BLUE, left_bar=False, pad=10))
story.append(Spacer(1, 10))
story.append(P("What the symbols mean", "h3"))
story.append(table([
    ["You'll see…", "It means…"],
    [f"{key('Cmd')} + {key('S')}", "Press these keys together (hold the first, tap the second)."],
    [menu("Kernel", "Restart Kernel and Run All Cells…"), "Click the <b>Kernel</b> menu, then that item."],
    ['<font color="white" backColor="#1E1E1E" name="Mono">&nbsp;black box&nbsp;</font>',
     f"A command: type it exactly (or copy-paste) into Terminal, then press {key('Enter')}."],
    ['<font color="#D9731F"><b>SCREENSHOT 3.4</b></font>', "Take a screenshot now and save it with the name shown."],
    ['<font color="#2F6FB3"><b>TIP</b></font> / <font color="#C0392B"><b>WATCH OUT</b></font>',
     "Helpful extra info / something that commonly goes wrong."],
    ['<b>On Windows:</b> grey box', "Only read it if you're on a Windows laptop – this guide is for a Mac."],
], [4.4 * cm, W - 4.4 * cm]))
story.append(Spacer(1, 10))
story.append(P("Time you'll need (roughly)", "h3"))
story.append(table([
    ["Part", "What you'll do", "Time"],
    ["0 · Setup", "Get the new files, install the Lab 1–3 libraries, make your .env key file", "≈ 20 min"],
    ["Week 1", "Ollama + Gemini key, run the Lab 1 notebook, screenshots", "≈ 45 min"],
    ["Week 2", "Hugging Face token, run the smolagents notebook (local model is slow)", "≈ 1 h"],
    ["Week 3", "Pinecone + Make.com (in the browser), then the Python RAG scripts", "≈ 1.5 h"],
    ["Week 4", "Separate Python 3.12 environment, run the AutoGen app + scripts", "≈ 45 min"],
    ["Finish", "Hand-in copies, save everything to GitHub", "≈ 15 min"],
], [2.4 * cm, W - 5.4 * cm, 3.0 * cm]))
story.append(PageBreak())

# ============================================================= tracker
story.append(P("Your progress tracker", "h1"))
story.append(P("Tick things off as you go.", "small"))
story.append(Spacer(1, 6))
tracker = [
    ("Part 0", ["New files downloaded (git pull)", "Lab 1–3 libraries installed", ".env file made (keys go in later)"]),
    ("Week 1", ["Ollama installed + llama3.2:1b in Terminal (1.1)", "Gemini key in .env (1.3)",
                "Lab1 notebook run (1.2, 1.4–1.6, 1.8)", "Gradio chat (1.7)", "Worklog finished + hand-in copy"]),
    ("Week 2", ["Hugging Face token in .env (2.1)", "smolagents installed (2.2)", "Lab2 notebook run (2.3–2.7)",
                "GradioUI chat (2.8)", "Worklog finished + hand-in copy"]),
    ("Week 3", ["Pinecone index + key in .env (3.1)", "Make: ingestion (3.2, 3.3)", "Make: query (3.4–3.6)",
                "Python: concept demo, ingest, query (3.7–3.11)", "experiments.py + make_check.py (3.12)",
                "Worklog finished + hand-in copy"]),
    ("Week 4", ["Python 3.12 environment + install (4.1)", "Fix screenshot (4.2)", "App + 4 examples (4.3–4.6)",
                "run_examples + groupchat_demo (4.7, 4.8)", "Worklog finished + hand-in copy"]),
    ("Finish", ["Everything pushed to GitHub", "Handed in what my tutor asked for"]),
]
rows = [["", "Task", "Done?"]]
for part, tasks in tracker:
    for i, t in enumerate(tasks):
        rows.append([f"<b>{part}</b>" if i == 0 else "", t, "☐"])
story.append(table(rows, [2.2 * cm, W - 4.0 * cm, 1.8 * cm]))
story.append(PageBreak())

# ============================================================= PART 0
story.append(band("Part 0 · Setup", "≈ 20 minutes · once for all four labs"))
story.append(Spacer(1, 8))
story += tip("You already did the big setup for Labs 5–9 (Python 3.12 + the <b>.venv</b> environment in "
             "<b>Documents › LabChallenge</b>). This part only adds what's new.")

story.append(P("0.1  Open Terminal in your LabChallenge folder", "h2"))
reset_steps()
story.append(step("Press " + key("Cmd") + " + " + key("Space") + ", type <b>Terminal</b>, press " + key("Enter") + "."))
story.append(step("Type " + mono("cd ") + " (with a space after it), then <b>drag your LabChallenge folder</b> from "
                  "Finder into the Terminal window, and press " + key("Enter") + ".",
                  P("Or type " + mono("cd ~/Documents/LabChallenge") + " if that's where it is.", "small")))
story.append(step("Switch your Python environment on:", cmd("source .venv/bin/activate"),
                  P("The line now starts with <b>(.venv)</b>. ✓ Do this every time you open a new Terminal window "
                    "for these labs (except Week 4, which has its own).", "small")))
story += win("open the LabChallenge folder in File Explorer, click the address bar, type " + mono("cmd") +
             " and press Enter; activate with " + mono(".venv\\Scripts\\activate") + ".")
story += tip("No <b>.venv</b> folder (e.g. a new laptop)? Make one: " + mono("python3.12 -m venv .venv") + ", then "
             + mono("source .venv/bin/activate") + " and " + mono("pip install notebook pandas matplotlib python-docx "
                                                              "pillow") + ".")

story.append(P("0.2  Get the new files", "h2"))
reset_steps()
story.append(step("Download everything I added (Labs 1–4 notebooks, scripts, worklogs):",
                  cmd(f"git checkout {BRANCH}", "git pull"),
                  P("You should now have <b>Lab 1 › Lab1_LLM_Access.ipynb</b>, <b>Lab 3 › simple-rag</b> and "
                    "<b>Lab 1 › Lab1_Worklog_Week1.docx</b> etc. If git complains about <b>local changes</b>, close Word "
                    "and run " + mono("git stash") + " first, then " + mono("git pull") + " again.", "small")))

story.append(P("0.3  Install the libraries for Labs 1 and 3", "h2"))
reset_steps()
story.append(step("With <b>(.venv)</b> on:",
                  cmd("pip install ollama google-genai python-dotenv requests gradio pinecone"),
                  P("Takes a minute. It ends with <b>Successfully installed …</b>. (Lab 2's smolagents gets installed "
                    "in Week 2 so you can screenshot it; Lab 4 gets its own environment.)", "small")))

story.append(P("0.4  Make your .env file (where your keys go)", "h2"))
story.append(P("Each week you'll create a free key on a website. They all go in one file called <b>.env</b> in the "
               "LabChallenge folder. Git ignores this file, so it never ends up on GitHub."))
reset_steps()
story.append(step("Make it from the template and open it in TextEdit:", cmd("cp .env.example .env", "open -e .env")))
story.append(step("You'll see lines like " + mono("GEMINI_API_KEY=your_gemini_api_key") + ". Leave it open – each "
                  "week you replace one <i>your_…</i> part with your real key (no spaces, no quotes) and save with "
                  + key("Cmd") + " + " + key("S") + "."))
story += win(mono("copy .env.example .env") + " then " + mono("notepad .env") + ".")
story += tip("Files starting with a dot are hidden in Finder. To see them press " + key("Cmd") + " + "
             + key("Shift") + " + " + key(".") + " in the Finder window.")
story += keys_warning()

story.append(P("0.5  Screenshots on a Mac", "h2"))
reset_steps()
story.append(step("Press " + key("Cmd") + " + " + key("Shift") + " + " + key("4") + " and drag a box around what the "
                  "guide asks for (make sure the text is readable)."))
story.append(step("The picture lands on your <b>Desktop</b> as <i>Screenshot 2026-…png</i>. Drag it into "
                  "<b>LabChallenge › Lab N › screenshots</b>, click its name once, press " + key("Enter") +
                  ", and type the name the guide gives (e.g. <b>1.1_ollama_cli</b>) – keep the <b>.png</b>."))
story += tip("Only the number at the start has to be exact (<b>1.1_</b>…). Something too long for one picture? "
             "Take two and name them <b>1.2a_…</b> and <b>1.2b_…</b> – both get inserted.")
story += win(key("Win") + " + " + key("Shift") + " + " + key("S") + ", click the pop-up, then save "
             "(Ctrl + S) straight into the screenshots folder.")

story.append(P("0.6  Two Terminal tabs", "h2"))
story.append(table([
    ["Tab", "Used for"],
    ["<b>Tab 1</b>", "Runs <b>Jupyter</b> (" + mono("jupyter notebook") + "). Once it's started leave it alone – don't "
                     "close it, don't type in it."],
    ["<b>Tab 2</b>", "Everything else. Open it with " + key("Cmd") + " + " + key("T") + ", then do 0.1 again "
                     "(cd + activate)."],
], [2.4 * cm, W - 2.4 * cm]))
story.append(PageBreak())

# ============================================================= WEEK 1
story.append(band("Week 1 · LLM access – local + cloud", "≈ 45 minutes · Lab 1 · dates in your worklog: 2–9 Aug"))
story.append(Spacer(1, 8))
story += plain("An <b>LLM</b> (like ChatGPT) can run in two places: on <b>your own laptop</b> (free, private, but "
               "small) or in the <b>cloud</b> (big and fast, but you need an account and a key). You run the same "
               "questions on both – a small model with <b>Ollama</b> and Google's <b>Gemini</b> – and compare speed, "
               "cost and quality. The notebook does all the measuring for you.")

story.append(P("1A  Install Ollama and chat in Terminal", "h2"))
reset_steps()
story.append(step("Go to <b>ollama.com/download</b> → <b>Download for macOS</b>. Open the download, drag <b>Ollama</b> "
                  "into <b>Applications</b>, then open it from Applications (click <b>Open</b> if the Mac asks). A "
                  "llama icon appears at the top of the screen – leave Ollama running."))
story.append(step("In <b>Tab 2</b>:", cmd("ollama run llama3.2:1b"),
                  P("First time it downloads ~1.3 GB (<i>pulling …</i> lines, then <b>success</b>). Then you get "
                    "<b>&gt;&gt;&gt;</b> – type " + mono("hello") + " and press " + key("Enter") + ".", "small")))
story += shot("1.1", "1.1_ollama_cli.png", "The Terminal window: the <i>pulling … success</i> lines and the model's "
                                           "reply to <b>hello</b>.")
story.append(step("Type " + mono("/bye") + " and press " + key("Enter") + " to leave the chat."))

story.append(P("1B  Make your Gemini key", "h2"))
reset_steps()
story.append(step("Go to <b>aistudio.google.com/app/api-keys</b> and sign in with your Google account (accept the "
                  "terms if asked)."))
story.append(step("Click <b>Create API key</b> → give it a name (e.g. <i>COS30018</i>) → choose the default project → "
                  "<b>Create key</b>. Click the copy icon next to the key."))
story.append(step("In your <b>.env</b> file (TextEdit), replace <i>your_gemini_api_key</i> with the key → "
                  + key("Cmd") + " + " + key("S") + "."))
story += warn("Your old key was typed into your Lab 1 notebook, so treat it as leaked: on the API keys page click "
              "the bin/delete icon next to it, then make a new one (step 2) and use only the new one.", "OLD KEY")
story += shot("1.3", "1.3_ai_studio_key.png", "The API keys page with your key in the list – it only shows the last "
                                               "few characters, that's fine. <b>Not</b> the pop-up that shows the full key.")

story.append(P("1C  Your completed notebook", "h2"))
story.append(P("You've already done the Lab 1 notebook yourself. <b>Lab 1 › Lab1_completed.ipynb</b> is your notebook "
               "with only one change: the API key is taken out (it had been typed into the code). Your Week 1 "
               "worklog is already filled in from its outputs, so there's nothing to re-run."))
reset_steps()
story.append(step("In <b>Tab 1</b> (in LabChallenge, (.venv) on):", cmd("jupyter notebook"),
                  P("Your browser opens Jupyter. (If not, copy the <b>http://localhost:8888/…</b> line into the "
                    "browser.)", "small")))
story.append(step("Click <b>Lab 1</b> → <b>Lab1_completed.ipynb</b>. <b>Don't</b> use Run All – the outputs are your "
                  "results. (If you do re-run it, the times change and the worklog needs the new numbers.)"))
story.append(step("In the last cell (<b>Checkpoint Questions</b>) double-click, replace your table and answers with "
                  "the corrected ones from your worklog (\"Deliverable – comparison table\" + \"Checkpoint "
                  "questions\"), then press " + key("Shift") + " + " + key("Enter") + " and save with "
                  + key("Cmd") + " + " + key("S") + "."))
story.append(step("Take these screenshots from the notebook:"))
story += shot("1.2", "1.2_ollama_notebook.png", "The <b>import ollama</b> + <b>ollama.chat(…)</b> cells and the start "
                                                 "of the answer to 'What is an intelligent system?'.")
story += shot("1.4", "1.4_gemini_notebook.png", "The <b>genai.Client()</b> + <b>generate_content</b> cells and the start "
                                                 "of Gemini's answer (no key visible in this copy).")
story += shot("1.5", "1.5_count_both_models.png", "Both counting functions' <b>Latency: 1.32s</b> / <b>Latency: 3.18s</b> "
                                                   "lines and both answers. Two pictures OK: 1.5a_…, 1.5b_….")
story += shot("1.6", "1.6_reasoning.png", "The four apple cells with their Latency lines and answers. Two pictures OK: "
                                          "1.6a_…, 1.6b_….")
story += shot("1.8", "1.8_comparison_table.png", "The Checkpoint Questions cell with the corrected comparison table.")
story.append(step("The chat window: click the <b>import ollama</b> cell near the top and press " + key("Shift") + " + "
                  + key("Enter") + ", then do the same for the three Gradio cells at the bottom. Open "
                  "<b>http://127.0.0.1:7860</b> and ask it something."))
story += shot("1.7", "1.7_gradio_chat.png", "The 'Week 1: Local LLM Chat (Ollama)' page with an answer.")
story += finish_week(1, [10])
story.append(PageBreak())

# ============================================================= WEEK 2
story.append(band("Week 2 · An agent with tools and memory", "≈ 1 hour · Lab 2 · dates in your worklog: 10–16 Aug"))
story.append(Spacer(1, 8))
story += plain("Instead of just asking a model a question, an <b>agent</b> can use <b>tools</b> (here: web search) "
               "and works in a loop: it <b>thinks</b>, writes some <b>code</b>, looks at the <b>result</b>, and repeats "
               "until it has the answer. The <b>smolagents</b> library runs that loop for you. You run it with a big "
               "cloud model (via Hugging Face) and a small model on your laptop, and compare.")

story.append(P("2A  Hugging Face token", "h2"))
reset_steps()
story.append(step("Make a free account at <b>huggingface.co</b> (confirm your email)."))
story.append(step("Click your profile picture (top right) → <b>Settings</b> → <b>Access Tokens</b> → "
                  "<b>+ Create new token</b> → choose <b>Read</b> → name it (e.g. <i>COS30018</i>) → "
                  "<b>Create token</b> → <b>Copy</b> (it's only shown once!)."))
story.append(step("In <b>.env</b> replace <i>hf_your_token</i> with it → save."))
story += shot("2.1", "2.1_hf_token.png", "The Access Tokens page with your token in the list (value hidden). Not the "
                                         "pop-up that shows the full token.")

story.append(P("2B  Install smolagents", "h2"))
reset_steps()
story.append(step("In <b>Tab 2</b> ((.venv) on):", cmd('pip install "smolagents[toolkit]" "smolagents[transformers]"'),
                  P("This one is big (it brings PyTorch + transformers if you don't have them) – a few minutes.",
                    "small")))
story += shot("2.2", "2.2_pip_install.png", "The end of the install (<b>Successfully installed …</b>).")
story += tip("If Jupyter was already running, restart it after installing: in Tab 1 press " + key("Ctrl") + " + "
             + key("C") + ", then " + mono("jupyter notebook") + " again.")

story.append(P("2C  Run the Lab 2 notebook", "h2"))
reset_steps()
story.append(step("In Jupyter open <b>Lab 2</b> → <b>Lab2_smolagents_agent.ipynb</b> → " +
                  menu("Kernel", "Restart Kernel and Run All Cells…") + "."))
story.append(step("Wait. The cloud parts take seconds; <b>Step 5 (local model) downloads ~3 GB the first time and then "
                  "runs on your CPU</b> – it can take 10+ minutes. If it fails, that's OK (the sheet says it might) – "
                  "the error is saved and goes into your worklog.",
                  tip("Laptop with only 8 GB of memory, or no time? Change " + mono("RUN_LOCAL = True") + " to "
                      + mono("RUN_LOCAL = False") + " in the first code cell and run all again – the worklog will say "
                      "you skipped it.")))
story.append(step("When the last cell prints <b>saved results/lab2_results.json</b>, take the screenshots:"))
story += shot("2.3", "2.3_no_tools.png", "Step 2: the <b>New run</b> box, Step 1 / Step 2 with the code, "
                                         "<b>Final answer: 1275</b>, and the small table.")
story += shot("2.4", "2.4_web_search.png", "Step 3: Step 1 with <b>web_search(…)</b> + its Execution logs, and Step 2 "
                                           "with the 15% maths + Final answer. Two pictures OK: 2.4a_…, 2.4b_….")
story += shot("2.5", "2.5_memory.png", "Step 4 output (TaskStep / ActionStep lines + 'what smolagents records') and the "
                                       "follow-up's last line (<i>searched again: False …</i>).")
story += shot("2.6", "2.6_local_model.png", "Step 5: <b>loaded Qwen/… in … s</b>, the steps and the answer (or the "
                                            "error).")
story += shot("2.7", "2.7_cloud_vs_local.png", "Step 6: the <b>Cloud: …s</b> / <b>Local: …s</b> lines and the "
                                               "comparison table.")
story.append(step("Open the link printed under Step 7 (usually <b>http://127.0.0.1:7860</b>, or 7861 if the Week 1 chat "
                  "is still running). Ask something that needs a search, e.g. <i>What's the population of "
                  "Sydney? Then divide it by 4.</i>"))
story += shot("2.8", "2.8_gradio_ui.png", "The GradioUI chat with the agent's steps and the final answer.")
story += warn("Cloud model error like <b>402</b>, <b>credits</b> or <b>quota</b>? Hugging Face's free monthly credit "
              "ran out – wait until next month or try again tomorrow; everything else still works.")
story += finish_week(2, [11])
story.append(PageBreak())

# ============================================================= WEEK 3
story.append(band("Week 3 · RAG with a vector database", "≈ 1.5 hours · Lab 3 · dates in your worklog: 17–23 Aug"))
story.append(Spacer(1, 8))
story += plain("<b>RAG</b> = before answering, look up the right part of <i>your own documents</i> and give it to the "
               "model. Step 1 (<b>ingestion</b>): cut the text into chunks, turn each chunk into numbers (an "
               "<b>embedding</b>) and store them in <b>Pinecone</b>. Step 2 (<b>query</b>): turn the question into "
               "numbers, find the most similar chunks, and let Gemini answer only from them. You build it twice: "
               "first by clicking in <b>Make.com</b>, then in <b>Python</b>.")

story.append(P("3A  Pinecone (the vector database)", "h2"))
reset_steps()
story.append(step("Sign up for free at <b>pinecone.io</b> (the free <i>Starter</i> plan)."))
story.append(step("Click <b>Create index</b>. Name: <b>intelligent-systems</b>. Choose the custom / manual settings: "
                  "<b>Vector type: Dense</b>, <b>Dimension: 1024</b>, <b>Metric: cosine</b>. Capacity: "
                  "<b>Serverless</b>, <b>AWS</b>, <b>us-east-1</b>. Click <b>Create index</b>.",
                  warn("The dimension <b>must be 1024</b> – it has to match the embeddings in both the Make blueprints "
                       "and the Python code.")))
story += shot("3.1", "3.1_pinecone_index.png", "Your index page showing dimension 1024, metric cosine, dense.")
story.append(step("Left menu → <b>API Keys</b> → <b>Create API key</b> → copy it. In <b>.env</b>: "
                  + mono("PINECONE_API_KEY=") + "the key, and " + mono("PINECONE_INDEX=intelligent-systems") + " → save."))
story += tip("Python way to make the index instead: " + mono("cd \"Lab 3/simple-rag\"") + " then "
             + mono("python setup_index.py") + " (after the key is in .env). You still need screenshot 3.1.")

story.append(P("3B  Make.com – Part 1: ingestion", "h2"))
reset_steps()
story.append(step("Upload the text file to your Google Drive: <b>drive.google.com</b> → <b>+ New</b> → <b>File upload</b> → "
                  "pick <b>LabChallenge › Lab 3 › intelligent_agents_overview.txt</b>."))
story.append(step("Sign up for free at <b>make.com</b>. Go to <b>Scenarios</b> → <b>+ Create a new scenario</b>."))
story.append(step("Click the <b>⋯</b> (three dots) button → <b>Import blueprint</b> → choose "
                  "<b>Lab 3 › RAG Ingestion.blueprint.json</b> → <b>Save</b>. Five modules appear."))
story.append(step("The blueprint still has the tutor's accounts, so click each module and connect yours:",
                  P("• <b>Google Drive</b> → Connection: <b>Add</b> → sign in with Google → allow. Then for <b>File</b> "
                    "pick your uploaded <i>intelligent_agents_overview.txt</i>.<br/>"
                    "• <b>Google Gemini AI</b> → Connection: <b>Add</b> → paste your Gemini key (same as .env). Check "
                    "<b>Output dimensionality = 1024</b>.<br/>"
                    "• <b>Pinecone</b> → Connection: <b>Add</b> → paste your Pinecone key; choose your index if it asks. "
                    "Check namespace <b>week3-lab</b>.<br/>"
                    "Click <b>OK</b> on each, then save the scenario (" + key("Cmd") + " + " + key("S") + ")."),
                  keys_warning()))
story.append(step("Click <b>Run once</b> (bottom left). Each module gets a green tick and a bubble with a number."))
story += shot("3.2", "3.2_make_ingestion.png", "The scenario after Run once – all 5 modules with ticks and bubbles.")
story.append(step("Pinecone console → your index → <b>Browser</b> tab → Namespace <b>week3-lab</b> → click a record "
                  "so you can see its <b>text</b> and <b>source</b>."))
story += shot("3.3", "3.3_make_pinecone_record.png", "<b>(deliverable)</b> A record from namespace <b>week3-lab</b> "
                                                     "with its ID and <b>text</b> + <b>source</b> metadata.")

story.append(P("3C  Make.com – Part 2: query", "h2"))
reset_steps()
story.append(step("New scenario → <b>⋯</b> → <b>Import blueprint</b> → <b>Lab 3 › RAG Query.blueprint.json</b>. "
                  "Connect your accounts again (both Gemini modules + Pinecone), like in 3B."))
story.append(step("Click the first module (<b>Set variable</b>) → change the value to <b>What is a learning agent?</b> "
                  "→ OK → <b>Run once</b>. Click the bubble on the <b>last</b> module to see the answer."))
story += shot("3.4", "3.4_make_query_answer.png", "<b>(deliverable)</b> The query scenario after Run once, with the "
                                                  "answer bubble open (like the last picture in the Make sheet).")
story.append(step("Change the question to <b>What's the weather in Melbourne?</b> → Run once → open the answer."))
story += shot("3.5", "3.5_make_out_of_scope.png", "The answer saying it doesn't have enough information.")
story.append(step("The modification: question back to <b>What is a learning agent?</b>, click the <b>Pinecone</b> "
                  "module → change <b>Limit</b> from 3 to <b>1</b> → OK → Run once. Then try <b>5</b>. Put it back to 3 "
                  "afterwards."))
story += shot("3.6", "3.6_make_limit_change.png", "The Pinecone module settings with the new Limit + the answer bubble "
                                                  "after running. Two pictures OK: 3.6a_…, 3.6b_….")

story.append(P("3D  Python – the same thing in code", "h2"))
reset_steps()
story.append(step("In <b>Tab 2</b> ((.venv) on, in LabChallenge):", cmd('cd "Lab 3/simple-rag"', "python concept_demo.py"),
                  P("Asks Gemini a question about the notes <b>without</b> and <b>with</b> the right chunk pasted in.",
                    "small")))
story += shot("3.7", "3.7_concept_demo.png", "The output: the answer with NO context and WITH the chunk.")
story.append(step("Part 1 – ingestion:", cmd("python ingest.py"),
                  P("Ends with <b>Ingestion complete.</b> and <b>Pinecone now has 9 records …</b>.", "small")))
story += shot("3.8", "3.8_ingest.png", "The ingest.py output (Loaded…, Created 9 chunks, Processing chunk 1/9 … 9/9, "
                                       "Ingestion complete).")
story.append(step("Pinecone console → Browser → namespace <b>week3-code-lab</b> → click a record."))
story += shot("3.9", "3.9_python_pinecone_record.png", "<b>(deliverable)</b> A record with <b>text</b>, <b>source</b> and "
                                                       "<b>chunk_number</b>.")
story.append(step("Part 2 – query:", cmd("python query.py"),
                  P("At <b>Ask a question:</b> type " + mono("What is a learning agent?") + " and press " + key("Enter")
                    + ".", "small")))
story += shot("3.10", "3.10_query_learning_agent.png", "<b>(deliverable)</b> The retrieved chunks (Rank, ID, Score, "
                                                       "Text) and the FINAL ANSWER. Two pictures OK: 3.10a_…, 3.10b_….")
story.append(step("The out-of-scope question:", cmd('python query.py "What\'s the weather in Melbourne?"')))
story += shot("3.11", "3.11_query_out_of_scope.png", "<b>(deliverable)</b> The low scores and the 'not enough "
                                                     "information' answer.")
story.append(step("The experiments (top-k 1/3/5, chunk size 100/400, more questions) – a few minutes:",
                  cmd("python experiments.py")))
story += shot("3.12", "3.12_experiments.png", "<b>(deliverable)</b> The Experiment A part and the Experiment B part of "
                                              "the output. Two pictures OK: 3.12a_…, 3.12b_….")
story.append(step("Check what Make stored and repeat its search with Limit 1/3/5 (this fills the Make part of your "
                  "worklog):", cmd("python make_check.py", "cd ../.."),
                  P("The last line takes you back to the LabChallenge folder.", "small")))
story += warn("<b>Model not found</b> / <b>404</b>? Google renamed a model – the scripts try the next one by "
              "themselves. <b>429 / rate limit</b>? They wait and retry; if it keeps happening, wait a few minutes "
              "and run that script again.")
story += finish_week(3, [7, 8, 13], "Items 7 and 8 are the Make query runs you did in 3C.")
story.append(PageBreak())

# ============================================================= WEEK 4
story.append(band("Week 4 · Multi-agent conversation (AutoGen)", "≈ 45 minutes · Lab 4 · dates in your worklog: "
                                                                 "24–30 Aug"))
story.append(Spacer(1, 8))
story += plain("Two AI <b>agents</b> talk to each other: the <b>assistant</b> writes Python code, the <b>userproxy</b> "
               "runs it on your laptop and reports back, until the job is done. It's the tutor's AutoGen app with a "
               "chat page. I fixed the bits that stopped it working with Gemini (they're listed in your worklog) and "
               "added a script that runs the examples for you, plus an extra agent (a <b>critic</b>).")
story += warn("This lab needs <b>its own environment with Python 3.12</b>: the tutor's "
              + mono("pyautogen==0.2.28") + " doesn't install on Python 3.13+, and its old Gradio version would break "
              "Labs 1–2 if you put it in .venv.", "WHY A SECOND ENVIRONMENT")

story.append(P("4A  Make the AutoGen environment", "h2"))
reset_steps()
story.append(step("In <b>Tab 2</b>, switch .venv off and make the new one (in the LabChallenge folder):",
                  cmd("deactivate", "python3.12 -m venv .venv-autogen", "source .venv-autogen/bin/activate"),
                  P("The line now starts with <b>(.venv-autogen)</b>. " + mono("python3.12: command not found") +
                    "? Install Python 3.12 from <b>python.org/downloads/macos</b> (Python 3.12.x, macOS installer) "
                    "and try again.", "small")))
story.append(step("Install the tutor's requirements + yfinance (for the stock example):",
                  cmd('cd "Lab 4/Multiagent"', "pip install -r requirements.txt yfinance", "python --version")))
story += shot("4.1", "4.1_venv_install.png", "<b>Successfully installed …</b> and <b>Python 3.12.x</b> from the last "
                                             "command.")
story += win(mono("py -3.12 -m venv .venv-autogen") + " and " + mono(".venv-autogen\\Scripts\\activate") + ".")

story.append(P("4B  Show the fix", "h2"))
reset_steps()
story.append(step("Open <b>Lab 4 › Multiagent › CONFIG_LIST.json</b> and <b>agent.py</b> (in VS Code, or right-click → "
                  "Open With → TextEdit). Your key is <b>not</b> in them – it comes from .env."))
story += shot("4.2", "4.2_config_fix.png", "CONFIG_LIST.json with the <b>base_url</b> line, and the <b>(my fix)</b> lines "
                                           "in agent.py. Two pictures OK: 4.2a_…, 4.2b_….")

story.append(P("4C  Run the app", "h2"))
reset_steps()
story.append(step("Still in <b>Lab 4/Multiagent</b> with (.venv-autogen):", cmd("python app.py"),
                  P("Wait for <b>Running on local URL: http://0.0.0.0:7868</b>.", "small")))
story += shot("4.3", "4.3_app_running.png", "The Terminal with the <b>Running on local URL</b> line.")
story.append(step("Open <b>http://127.0.0.1:7868</b> in your browser. Click the examples <b>one at a time, in order</b> "
                  "and wait for each answer (10–60 s)."))
story += shot("4.4", "4.4_example_sum.png", "Example 1: the assistant's code, the userproxy's <b>exitcode: 0</b>, the "
                                            "final answer.")
story += shot("4.5", "4.5_example_product.png", "Example 2 (<i>what if the production…</i>): it should use "
                                                "multiplication.")
story += shot("4.6", "4.6_example_stock_chart.png", "Example 3 (stock chart) and example 4 (<b>show file:</b> with the "
                                                    "chart in the chat). Two pictures OK: 4.6a_…, 4.6b_….")
story.append(step("Back in Terminal press " + key("Ctrl") + " + " + key("C") + " to stop the app."))

story.append(P("4D  The scripts that fill your worklog", "h2"))
reset_steps()
story.append(step("Run the 4 examples without the browser (saves the numbers + full conversations):",
                  cmd("python run_examples.py")))
story += shot("4.7", "4.7_run_examples.png", "The end of the output: the <b>--&gt; … s | … messages</b> line for each "
                                             "example and <b>saved …</b>.")
story.append(step("The extra agent – coder + critic + executor:", cmd("python groupchat_demo.py")))
story += shot("4.8", "4.8_groupchat.png", "<b>Next speaker: critic</b>, the critic's <b>APPROVED</b> (or its comments), "
                                          "the exit code and the summary line.")
story.append(step("Go back to the main environment for the worklog tools:",
                  cmd("deactivate", "cd ../..", "source .venv/bin/activate")))
story += warn("<b>Timeout Error</b> or an error about the key → check GEMINI_API_KEY in .env, then restart app.py. "
              "<b>No matching distribution for pyautogen</b> → you're not on Python 3.12 (redo 4A). The stock example "
              "says yfinance is missing → " + mono("pip install yfinance") + " in (.venv-autogen).")
story += finish_week(4, [5, 9], "Item 5 is trying the examples in the browser (4C).")
story.append(PageBreak())

# ============================================================= FINISH
story.append(band("Finish · hand in and save", "≈ 15 minutes"))
story.append(Spacer(1, 8))
reset_steps()
story.append(step("Open each <b>Completed Labs › Lab N Completed.docx</b> (N = 1–4) once and check: your name + ID at the "
                  "top, the dates, no yellow boxes or yellow text left, the screenshots are readable."))
story.append(step("If your tutor wants PDFs: in Word " + menu("File", "Save As…") + " → File Format <b>PDF</b>."))
story.append(step("Save everything to GitHub (your results, screenshots and worklogs – <b>.env is ignored</b>, so your "
                  "keys stay on your laptop):",
                  cmd("git add -A", 'git commit -m "Labs 1-4 results, screenshots and worklogs"', "git push"),
                  P("Before pushing, " + mono("git status") + " must <b>not</b> list a file called <b>.env</b>. "
                    "(It won't – it's in .gitignore.)", "small")))
story.append(step("Hand in what your tutor asked for (the worklogs, plus for Week 3 the deliverable screenshots and "
                  "notes – they're already inside your Week 3 worklog)."))
story += tip("A lot of this was prepared with an AI assistant. Read each worklog's answers so you can explain them "
             "yourself, and check your unit's rules on AI use – add an acknowledgement if they ask for one.")

story.append(P("Troubleshooting", "h1"))
story.append(table([
    ["What you see", "What to do"],
    ["<b>command not found: python</b>", "Use " + mono("python3") + " – or activate the environment first (the line "
                                         "must start with (.venv))."],
    ["<b>ModuleNotFoundError</b> in a notebook", "Jupyter was started without (.venv), or that week's install was "
     "skipped. In Tab 1: " + key("Ctrl") + " + " + key("C") + ", activate, install, " + mono("jupyter notebook") + "."],
    ["<b>KeyError</b> / 'No HF_TOKEN' / 'Missing GEMINI_API_KEY…'", "The key isn't in .env, .env isn't saved, or it's "
     "not in the LabChallenge folder. No spaces or quotes around the key."],
    ["<b>429</b> / <b>RESOURCE_EXHAUSTED</b> / rate limit", "Free-tier limit. The code waits and retries. If it says "
     "<b>per day</b>, the notebook switches to another Gemini model by itself; otherwise try tomorrow."],
    ["<b>404 … model not found</b>", "Google renamed a model. The notebooks/scripts move to the next one in their list "
     "automatically."],
    ["build_worklogs says <b>has been edited … NOT overwriting</b>", "You opened/changed the worklog (or inserted "
     "screenshots) before building it. Easiest fix: " + mono("git checkout -- \"Lab N/LabN_Worklog_WeekN.docx\"") +
     " (puts the original back), then build → insert screenshots → tick, in that order."],
    ["insert_screenshots says <b>still missing</b>", "File not in <b>Lab N › screenshots</b>, or the name doesn't start "
     "with the exact number (e.g. <b>3.10_</b>), or it isn't .png/.jpg."],
    ["<b>PermissionError</b> from a _tools command", "The worklog is open in Word – close it and run again."],
    ["Make.com: a module shows a red error", "Usually a connection: click the module → Connection → Add → paste your key "
     "again. For Google Drive, re-pick the file."],
    ["Pinecone: <b>dimension … does not match</b>", "The index isn't 1024. Make a new index with dimension 1024 and put "
     "its name in .env."],
    ["Port <b>7860</b> / <b>7868</b> already in use", "An old chat is still running. Close the old Jupyter/Terminal "
     "or use the other link Gradio prints."],
], [5.6 * cm, W - 5.6 * cm]))


# ============================================================= build
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont(BODY, 8)
    canvas.setFillColor(GREY)
    if doc.page > 1:
        canvas.drawString(1.8 * cm, A4[1] - 1.2 * cm, "COS30018 Labs 1–4 · click-by-click guide")
        canvas.setStrokeColor(colors.HexColor("#DDDDDD"))
        canvas.line(1.8 * cm, A4[1] - 1.35 * cm, A4[0] - 1.8 * cm, A4[1] - 1.35 * cm)
    canvas.drawRightString(A4[0] - 1.8 * cm, 1.1 * cm, f"page {doc.page}")
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm,
                            topMargin=1.7 * cm, bottomMargin=1.6 * cm,
                            title="COS30018 Labs 1-4 - click-by-click guide",
                            author="Prepared for Anas Al Azad", subject="How to finish Labs 1-4")
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
