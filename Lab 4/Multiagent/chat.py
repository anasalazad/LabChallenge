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
                "content": msg[1],
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
    ) < 2:

        chat_history.append(
            [
                user_message,
            ]
        )

        return chat_history

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

        if os.path.exists(filepath):

            chat_history.append(
                [
                    user_message,
                    (filepath,),
                ]
            )

        else:

            chat_history.append(
                [
                    user_message,
                    f"File {filename} not found.",
                ]
            )

        return chat_history

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

        chat_history += (
            message_to_chat(
                messages,
                assistant
            )
        )

    except Exception as e:

        chat_history.append(
            [
                user_message,
                str(e)
            ]
        )

    assistant._oai_system_message = (
        assistant
        ._oai_system_message_origin
        .copy()
    )

    if LOG_LEVEL == "DEBUG":
        print(
            f"chat_history: {chat_history}"
        )

    return chat_history


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

            messages = [
                input_text,
                (
                    "Timeout Error: Please check "
                    "your API keys and try again later."
                ),
            ]

    except Exception as e:

        messages = [
            [
                input_text,
                (
                    str(e)
                    if len(str(e)) > 0
                    else (
                        "Invalid Request to OpenAI, "
                        "please check your API keys."
                    )
                ),
            ]
        ]

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
    model,
    oai_key,
    aoai_key,
    aoai_base
):

    chat_history[:] = chatbot_reply(
        message,
        chat_history,
        config_list
    )

    if LOG_LEVEL == "DEBUG":
        print(
            f"return chat_history: {chat_history}"
        )

    return ""
