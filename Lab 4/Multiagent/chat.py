import os

from autogen import OpenAIWrapper

from agent import initialize_agents, config_list
from utils import *


assistant, userproxy = initialize_agents()


def chat_to_message(chat_history):
    """Convert chat history to OpenAI message format."""

    messages = []

    if LOG_LEVEL == "DEBUG":
        print(
            f"chat_to_oai_message: {chat_history}"
        )

    for msg in chat_history:
        messages.append(
            {
                "content": (
                    msg[0].split()[0]
                    if msg[0].startswith("exitcode")
                    else msg[0]
                ),
                "role": "user",
            }
        )

        messages.append(
            {
                # (my fix) a "show file:" reply is a file, not text - the model only needs to know that
                "content": (
                    msg[1]
                    if isinstance(msg[1], str)
                    else "[a file was shown in the chat]"
                ),
                "role": "assistant",
            }
        )

    return messages


def message_to_chat(messages, sender):
    """Convert OpenAI message format to chat history."""

    chat_history = []

    messages = messages[sender]

    if LOG_LEVEL == "DEBUG":
        print(
            f"message_to_chat: {messages}"
        )

    for i in range(0, len(messages), 2):
        chat_history.append(
            [
                messages[i]["content"],
                (
                    messages[i + 1]["content"]
                    if i + 1 < len(messages)
                    else ""
                ),
            ]
        )

    return chat_history


def initiate_chat(
    config_list,
    user_message,
    chat_history
):

    if LOG_LEVEL == "DEBUG":
        print(
            f"chat_history_init: {chat_history}"
        )

    if len(
        config_list[0].get("api_key", "")
    ) < 2 or config_list[0].get("api_key", "").startswith("Your"):

        # (my fix) the original appended a 1-item list, which the chat window can't display
        return (
            "No API key found - put GEMINI_API_KEY=... in the .env file "
            "(top folder of the repo) and restart app.py."
        )

    else:

        llm_config = {
            "timeout": TIMEOUT,
            "config_list": config_list,
        }

        assistant.llm_config.update(
            llm_config
        )

        assistant.client = OpenAIWrapper(
            **assistant.llm_config
        )

    if (
        user_message
        .strip()
        .lower()
        .startswith("show file:")
    ):

        filename = (
            user_message
            .strip()
            .lower()
            .replace("show file:", "")
            .strip()
        )

        filepath = os.path.join(
            "coding",
            filename
        )

        # (my fix) return the reply - gr.ChatInterface adds [message, reply] to the chat itself
        if os.path.exists(filepath):

            return (filepath,)

        else:

            return f"File {filename} not found."

    assistant.reset()

    oai_messages = chat_to_message(
        chat_history
    )

    assistant._oai_system_message_origin = (
        assistant
        ._oai_system_message
        .copy()
    )

    assistant._oai_system_message += (
        oai_messages
    )

    try:

        userproxy.initiate_chat(
            assistant,
            message=user_message
        )

        messages = (
            userproxy.chat_messages
        )

        # (my fix) the original added every message pair to chat_history AND returned "",
        # so gr.ChatInterface then added [message, ""] again at the bottom (the user's
        # message showed twice + an empty bubble). Now the whole agent conversation is
        # returned as ONE reply, with the name of the agent above each message.
        reply = format_conversation(
            message_to_chat(
                messages,
                assistant
            )
        )

    except Exception as e:

        reply = f"Error: {e}"

    assistant._oai_system_message = (
        assistant
        ._oai_system_message_origin
        .copy()
    )

    if LOG_LEVEL == "DEBUG":
        print(
            f"reply: {reply}"
        )

    return reply


def format_conversation(pairs):
    """(my addition) [[userproxy msg, assistant msg], ...] -> one Markdown reply.
    The first userproxy message is my own question, so it isn't repeated."""

    parts = []

    for i, (proxy_msg, assistant_msg) in enumerate(pairs):

        if i > 0 and proxy_msg:
            parts.append(
                "**🖥️ userproxy** (ran the code):\n\n```\n"
                + proxy_msg.strip()
                + "\n```"
            )

        if assistant_msg:
            parts.append(
                "**🤖 assistant:**\n\n" + assistant_msg.strip()
            )

    return "\n\n---\n\n".join(parts) or "(no reply)"


def chatbot_reply_thread(
    input_text,
    chat_history,
    config_list
):
    """Chat with the agent through terminal."""

    thread = thread_with_trace(
        target=initiate_chat,
        args=(
            config_list,
            input_text,
            chat_history
        )
    )

    thread.start()

    try:

        messages = thread.join(
            timeout=TIMEOUT
        )

        if thread.is_alive():

            thread.kill()

            thread.join()

            # (my fix) return a reply, not a half [input, text] pair
            messages = (
                f"Timeout Error: no answer within {TIMEOUT} s. Please check "
                "your API keys and try again later."
            )

    except Exception as e:

        messages = (
            str(e)
            if len(str(e)) > 0
            else (
                "Invalid Request to OpenAI, "
                "please check your API keys."
            )
        )

    return messages


def chatbot_reply(
    input_text,
    chat_history,
    config_list
):
    """Chat with the agent through terminal."""

    return chatbot_reply_thread(
        input_text,
        chat_history,
        config_list
    )


def chat_respond(
    message,
    chat_history,
    model=None,
    oai_key=None,
    aoai_key=None,
    aoai_base=None
):
    # (my fix) model / keys come from CONFIG_LIST.json + .env, so these are optional now
    # (app.py never passes them), and the reply is returned instead of ""

    reply = chatbot_reply(
        message,
        chat_history,
        config_list
    )

    if LOG_LEVEL == "DEBUG":
        print(
            f"return reply: {reply}"
        )

    return reply
