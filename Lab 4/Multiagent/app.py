import gradio as gr
from gradio import ChatInterface

from chat import chat_respond


LOG_LEVEL = "INFO"


with gr.Blocks() as demo:

    description = gr.Markdown(
        """
        # Microsoft AutoGen
        ## Multi-agent Conversation
        """
    )

    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(
            "../images/human.png",
            "../images/autogen.png",
        ),
        render=False,
        height=600,
    )

    txt_input = gr.Textbox(
        scale=4,
        show_label=False,
        placeholder="Enter text and press enter",
        container=False,
        render=False,
        autofocus=True,
    )

    chatiface = ChatInterface(
        chat_respond,
        chatbot=chatbot,
        textbox=txt_input,
        examples=[
            [
                "write a python function to count "
                "the sum of two numbers?"
            ],
            [
                "what if the production of two numbers?"
            ],
            [
                "Plot a chart of the last year's stock "
                "prices of Microsoft, Google and Apple "
                "and save to stock_price.png."
            ],
            [
                "show file: stock_price.png"
            ],
        ],
    )


if __name__ == "__main__":

    demo.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7868
    )
