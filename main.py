import os

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static, TextArea
from llama_cpp import Llama

from imagejenerator.models import registry

import config

max_threads = os.cpu_count()
if config.number_of_threads > max_threads:
    config.number_of_threads = max_threads

llm = Llama(
    model_path=config.path_to_model,
    n_ctx=config.max_context_size,
    n_threads=config.number_of_threads,
    verbose=config.verbose_warnings,
)

messages = [config.bot["system_prompt"]]
messages_all = [config.bot["system_prompt"]]

def generate_image(message):
    print("generating image")
    prompt = message[6:]
    print(prompt)
    config.image_config["prompts"][0] = prompt
    image_generator = registry.get_model_class(config.image_config)
    image_generator.generate_image()

splash = r"""       __           __          __ 
      / /__  ____  / /_  ____  / /_
 __  / / _ \/ __ \/ __ \/ __ \/ __/
/ /_/ /  __/ / / / /_/ / /_/ / /_  
\____/\___/_/ /_/_.___/\____/\__/  v1.0
"""


class ChatApp(App):
    def __init__(self):
        super().__init__()
        self.messages = [config.bot["system_prompt"]]
        self.messages_all = [config.bot["system_prompt"]]
    CSS = """
    Screen {
        layout: vertical;
    }

    #header {
        height: 5;
        content-align: left middle;
        background: black;
        color: white;
        text-style: bold;
    }

    #chat-container {
        height: 1fr;
        padding: 1;
        border: solid cyan;
    }

    #input {
        height: 8;
        border: solid #FF13F0;
    }

    .message {
        margin: 0 0 1 0;
    }
    """

    BINDINGS = [
        ("ctrl+enter", "submit_message", "Send"),
    ]

    def compose(self) -> ComposeResult:
        yield Static(splash, id="header")
        yield VerticalScroll(
            Static("Hi! Paste or type a message, Ctrl+Enter to submit.\n- type IMAGE <prompt> to generate image or ask Jenbot to do it. image_config must be defined and a diffusion model available locally at image_config['model_path'].\n- Ctrl+q to exit", classes="message"),
            id="chat-container"
        )
        yield TextArea("", id="input")

    def action_submit_message(self) -> None:
        chat = self.query_one("#chat-container", VerticalScroll)
        input_box = self.query_one("#input", TextArea)

        user_input = input_box.text.strip()
        if not user_input:
            return
        chat.mount(Static(f"[bold #FF13F0]You:[/] {user_input}\n", classes="message"))

        if config.image_config:
            if user_input[0:5] == "IMAGE":
                try:
                    generate_image(user_input)
                    chat.mount(Static(f"Image generated, see outputs folder", classes="message"))
                    return
                except Exception as e:
                    print("failed: ", e)
                    return

        # keep track of user input
        self.messages.append({"role": "user", "content": user_input})

        # call the LLM and generate response
        output = llm.create_chat_completion(
            messages=self.messages,
            max_tokens=config.max_tokens_per_response,
            temperature=config.temperature,
            top_p=config.top_p,
            top_k=config.top_k,
        )
        choice = output["choices"][0]["message"]
        output_text = (choice.get("content") or "").strip()
        if not output_text:
            output_text = "[No response generated.]"

        output_text_lines = output_text.split("\n")
        for output_text_line in output_text_lines:
            if output_text_line[0:5] == "IMAGE":
                try:
                    generate_image(output_text_line)
                except Exception as e:
                    print("failed: ", e)

        # keep track of bot responses
        self.messages.append({"role": "assistant", "content": output_text})

        # to keep responses faster, limit the number of messages we put in the context
        if len(messages) > config.messages_to_keep_in_context:
            if config.messages_to_keep_in_context == 0:
                self.messages = [config.bot["system_prompt"]]
            else:
                self.messages = [config.bot["system_prompt"]] + self.messages[-config.messages_to_keep_in_context:]


        
        chat.mount(Static(f"[bold cyan]{config.bot['name']}[/]: {output_text}\n\n"))

        input_box.text = ""
        chat.scroll_end(animate=False)


if __name__ == "__main__":
    ChatApp().run()
