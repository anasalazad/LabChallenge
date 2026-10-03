import os

import autogen
from autogen import AssistantAgent, UserProxyAgent
from autogen.code_utils import extract_code
from dotenv import load_dotenv


TIMEOUT = 60


config_list = autogen.config_list_from_json(
    "./CONFIG_LIST.json"
)

# (my fix) CONFIG_LIST.json is on GitHub, so the real key can't go in it.
# The "Your API Key" placeholder is swapped for GEMINI_API_KEY from the .env file
# (load_dotenv looks in this folder and the folders above it).
# The "base_url" in CONFIG_LIST.json sends AutoGen's OpenAI-style requests to Gemini's
# OpenAI-compatible endpoint - without it they go to api.openai.com and a Gemini key is rejected.
load_dotenv()
for config in config_list:
    if config.get("api_key", "").startswith("Your") and os.getenv("GEMINI_API_KEY"):
        config["api_key"] = os.environ["GEMINI_API_KEY"]


def _is_termination_msg(message):
    if isinstance(message, dict):
        message = message.get("content")

    if message is None:
        return False

    cb = extract_code(message)

    contain_code = False

    for c in cb:
        if c[0] == "python":
            contain_code = True
            break

    return not contain_code


def initialize_agents():
    assistant = AssistantAgent(
        name="assistant",
        max_consecutive_auto_reply=5,
        llm_config={
            "timeout": TIMEOUT,
            "config_list": config_list,
        },
    )

    userproxy = UserProxyAgent(
        name="userproxy",
        human_input_mode="NEVER",
        is_termination_msg=_is_termination_msg,
        max_consecutive_auto_reply=5,
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False,
        },
    )

    return assistant, userproxy
