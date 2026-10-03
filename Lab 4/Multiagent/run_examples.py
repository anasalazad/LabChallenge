"""(my addition) Run the app's 4 example prompts without the browser and save what happened.

Uses exactly the same code as the chat window (chat.chat_respond), one prompt after the other, with
the chat history passed along like the UI does - so "what if the production of two numbers?" can
refer back to the first answer.

    cd "Lab 4/Multiagent"
    python run_examples.py

Saves ../results/lab4_results.json (numbers for my worklog) and ../results/lab4_transcripts.md
(the full agent conversations).
"""
import json
import os
import re
import shutil
import time
from pathlib import Path

# AutoGen 0.2 caches every model reply in .cache/41 - delete it so each run really calls Gemini
shutil.rmtree(".cache", ignore_errors=True)

from agent import config_list   # noqa: E402  (after the cache is cleared)
from chat import assistant, chat_respond, userproxy   # noqa: E402

EXAMPLES = [
    "write a python function to count the sum of two numbers?",
    "what if the production of two numbers?",
    "Plot a chart of the last year's stock prices of Microsoft, Google and Apple and save to stock_price.png.",
    "show file: stock_price.png",
]
RESULTS = Path(__file__).resolve().parent.parent / "results"


def summarise(prompt, reply, seconds):
    """Count what happened inside one conversation (from the agents' own message lists)."""
    msgs = userproxy.chat_messages.get(assistant, []) if not prompt.startswith("show file") else []
    texts = [m.get("content") or "" for m in msgs]
    exitcodes = [int(c) for t in texts for c in re.findall(r"exitcode: (\d+)", t)]
    code_blocks = [t.count("```python") + t.count("```py\n") for t in texts]
    other_blocks = [len(re.findall(r"```(?:sh|bash|shell|console)", t)) for t in texts]
    last = texts[-1] if texts else ""
    return {
        "prompt": prompt,
        "seconds": round(seconds, 1),
        "messages": len(texts),
        "assistant_turns": len(texts[1::2]),
        "code_runs": len(exitcodes),
        "exitcodes": exitcodes,
        "python_blocks": sum(code_blocks),
        "shell_blocks": sum(other_blocks),
        "ended_with_terminate": "TERMINATE" in last,
        "hit_max_replies": len(texts) >= 2 * 5 + 1,
        "timeout": isinstance(reply, str) and reply.startswith("Timeout Error"),
        "error": isinstance(reply, str) and (reply.startswith("Error") or "check your API keys" in reply),
        "reply_is_file": isinstance(reply, tuple),
        "reply": reply if isinstance(reply, str) else f"[file: {reply[0]}]",
    }


def main():
    history, runs = [], []
    print(f"model: {config_list[0]['model']} via {config_list[0].get('base_url', 'api.openai.com')}\n")
    for prompt in EXAMPLES:
        print("=" * 80, f"\nYOU: {prompt}\n" + "=" * 80)
        start = time.time()
        reply = chat_respond(prompt, history)
        took = time.time() - start
        runs.append(summarise(prompt, reply, took))
        print(reply if isinstance(reply, str) else f"[shows the file {reply[0]}]")
        r = runs[-1]
        print(f"\n--> {took:.1f} s | {r['messages']} messages | code run {r['code_runs']} time(s), "
              f"exit codes {r['exitcodes']} | ended with TERMINATE: {r['ended_with_terminate']}\n")
        history.append([prompt, reply])   # like gr.ChatInterface does

    png = Path("coding") / "stock_price.png"
    out = {"run_at": time.strftime("%Y-%m-%d %H:%M"), "model": config_list[0]["model"],
           "base_url": config_list[0].get("base_url"), "runs": runs,
           "stock_png": png.exists(), "coding_files": sorted(os.listdir("coding")) if os.path.isdir("coding") else []}
    RESULTS.mkdir(exist_ok=True)
    data = json.loads((RESULTS / "lab4_results.json").read_text()) if (RESULTS / "lab4_results.json").exists() else {}
    data["examples"] = out
    (RESULTS / "lab4_results.json").write_text(json.dumps(data, indent=2))
    if png.exists():                          # the chart the agents made goes into my worklog
        figures = RESULTS.parent / "figures"
        figures.mkdir(exist_ok=True)
        shutil.copy(png, figures / "4_1_stock_price.png")

    md = [f"# Lab 4 – the app's example prompts ({out['run_at']}, {out['model']})\n"]
    for prompt, (p, reply) in zip(EXAMPLES, history):
        md.append(f"## You: {prompt}\n\n" + (reply if isinstance(reply, str) else f"[shows the file {reply[0]}]") + "\n")
    (RESULTS / "lab4_transcripts.md").write_text("\n".join(md), encoding="utf-8")
    print("saved ../results/lab4_results.json and ../results/lab4_transcripts.md"
          + (" + ../figures/4_1_stock_price.png" if png.exists() else ""))


if __name__ == "__main__":
    main()
