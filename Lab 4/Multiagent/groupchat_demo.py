"""(my addition) Extension: three agents instead of two, using AutoGen's GroupChat.

    coder    - AssistantAgent, writes the Python code (same as `assistant` in agent.py)
    critic   - AssistantAgent with its own system message: reviews the code, never writes any
    executor - UserProxyAgent, runs the code locally in coding/ (same as `userproxy` in agent.py)

They take turns in a fixed order (round robin: coder -> critic -> executor -> coder ...), so it
doesn't cost extra model calls to pick the next speaker. The chat stops when the coder says
TERMINATE or after MAX_ROUND messages.

    cd "Lab 4/Multiagent"
    python groupchat_demo.py

Saves ../results/lab4_results.json ("groupchat") and ../results/lab4_groupchat.md.
"""
import json
import re
import shutil
import time
from pathlib import Path

from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent

from agent import TIMEOUT, config_list

TASK = ("Write a Python function is_palindrome(text) that ignores spaces, punctuation and capital letters. "
        "Test it on 'Never odd or even', 'A man, a plan, a canal: Panama!' and 'Intelligent Systems' and print "
        "the results.")
MAX_ROUND = 10
RESULTS = Path(__file__).resolve().parent.parent / "results"

shutil.rmtree(".cache", ignore_errors=True)    # AutoGen caches replies - start fresh so it really runs
llm_config = {"timeout": TIMEOUT, "config_list": config_list}


def name_into_content(messages):
    """Group chat messages carry a "name" field. Not every OpenAI-compatible API accepts it, so put the
    speaker's name in front of the text instead (the agents can still see who said what)."""
    out = []
    for m in messages:
        m = dict(m)
        name = m.pop("name", None)
        if name and isinstance(m.get("content"), str) and m.get("role") == "user":
            m["content"] = f"[{name}] {m['content']}"
        out.append(m)
    return out


coder = AssistantAgent(name="coder", llm_config=llm_config)
critic = AssistantAgent(
    name="critic",
    llm_config=llm_config,
    system_message=(
        "You are a code reviewer in a team. Look at the latest code the coder wrote. If it is correct and safe "
        "to run, reply with 'APPROVED' and one short sentence why. If not, list the problems in at most 3 short "
        "bullet points. Never write code yourself and never say TERMINATE."
    ),
)
executor = UserProxyAgent(
    name="executor",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding", "use_docker": False, "last_n_messages": "auto"},
    default_auto_reply="(no code to run)",
)
for agent in (coder, critic):
    agent.register_hook("process_all_messages_before_reply", name_into_content)

groupchat = GroupChat(agents=[executor, coder, critic], messages=[], max_round=MAX_ROUND,
                      speaker_selection_method="round_robin")
manager = GroupChatManager(
    groupchat=groupchat, llm_config=llm_config,
    is_termination_msg=lambda m: "TERMINATE" in (m.get("content") or ""),
)

start = time.time()
executor.initiate_chat(manager, message=TASK)
took = time.time() - start

msgs = groupchat.messages
by_agent = {}
for m in msgs:
    by_agent[m.get("name", "?")] = by_agent.get(m.get("name", "?"), 0) + 1
critic_said = [m.get("content") or "" for m in msgs if m.get("name") == "critic"]
exitcodes = [int(c) for m in msgs if m.get("name") == "executor" for c in re.findall(r"exitcode: (\d+)", m.get("content") or "")]
summary = {
    "task": TASK, "seconds": round(took, 1), "messages": len(msgs), "by_agent": by_agent,
    "critic_approved_first_time": bool(critic_said) and "APPROVED" in critic_said[0].upper(),
    "critic_reviews": len(critic_said), "critic_first": critic_said[0][:300] if critic_said else "",
    "exitcodes": exitcodes, "ended_with_terminate": any("TERMINATE" in (m.get("content") or "") for m in msgs),
    "run_at": time.strftime("%Y-%m-%d %H:%M"), "model": config_list[0]["model"],
}
print(f"\n{len(msgs)} messages in {took:.1f} s | per agent: {by_agent} | exit codes: {exitcodes} | "
      f"critic approved first time: {summary['critic_approved_first_time']}")

RESULTS.mkdir(exist_ok=True)
path = RESULTS / "lab4_results.json"
data = json.loads(path.read_text()) if path.exists() else {}
data["groupchat"] = summary
path.write_text(json.dumps(data, indent=2))
md = [f"# Lab 4 extension – coder + critic + executor ({summary['run_at']}, {summary['model']})\n"]
md += [f"**{m.get('name', '?')}:**\n\n{m.get('content') or ''}\n\n---\n" for m in msgs]
(RESULTS / "lab4_groupchat.md").write_text("\n".join(md), encoding="utf-8")
print("saved ../results/lab4_results.json and ../results/lab4_groupchat.md")
