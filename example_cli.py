import os
import json
import yaml
from datetime import datetime
import textwrap

from textual.widgets import Markdown
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static, TextArea
from textual import events
import requests

from audiorecorder.audio_recorder import AudioRecorder
from sttjenerator.models import registry

from jenbot.core.orchestrator import Orchestrator


class ChatInput(TextArea):
    def _on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            event.prevent_default()
            self.app.action_submit_message()
            return

        if (event.key == "ctrl+j") or (event.key == "alt+enter"):
            self.insert("\n")
            event.prevent_default()
            return


class ChatMessage(Static):
    def __init__(self, text: str, **kwargs):
        super().__init__(text, **kwargs)
        self.text_content = text
    DEFAULT_CSS = """
    ChatMessage {
        background: #222222;
        margin-bottom: 2;
    }
    """

    def on_double_click(self) -> None:
        self.app.copy_to_clipboard(self.text_content)
        self.app.notify("Copied message to clipboard!")


with open("configs/core.yaml", 'r') as stream:
    core_config = yaml.safe_load(stream)
orchestrator = Orchestrator(core_config)


with open("configs/interface.yaml", 'r') as stream:
    interface_config = yaml.safe_load(stream)


class ChatApp(App):
    def __init__(self, orchestrator, interface_config, **kwargs):
        super().__init__(**kwargs)
        self.config = interface_config
        self.orchestrator = orchestrator
        self.stt_generator = self.load_stt_generator()
        self.audio_recorder = self.load_audio_recorder()
        self.splash = r"""       __           __          __ 
      / /__  ____  / /_  ____  / /_
 __  / / _ \/ __ \/ __ \/ __ \/ __/
/ /_/ /  __/ / / / /_/ / /_/ / /_  
\____/\___/_/ /_/_.___/\____/\__/  v1.0
"""

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
        border-left: none;
        border-right: none;
    }

    #input {
        height: 8;
        border-top: solid #FF13F0;
        border-bottom: solid #FF13F0;
        border-left: none;
        border-right: none;
    }

    #text-area {
        height: 8;
        border-left: none;
        border-right: none;
    }

    .message {
        margin: 0 0 1 0;
    }


    """
    def on_mount(self) -> None:
        self.query_one(ChatInput).focus()

    def compose(self) -> ComposeResult:
        yield Static(self.splash, id="header")
        yield VerticalScroll(
            Static("Hi!\n- type a message into the box below\n- Enter to submit.\n- ctrl+j for new line. alt+enter may work in some terminals\n- Shift+Ctrl+Click & Drag to select, then Shift+Ctrl+C to copy\n- Ctrl+q to exit", classes="message"),
            id="chat-container"
        )
        yield ChatInput("", id="input")


    def check_action(self, action: str, parameters: tuple) -> bool | None:
        chat_box = self.query_one("#input", TextArea)

        if self.focused == chat_box:
            if action == "submit_message":
                self.action_submit_message()
                return False

            if action == "insert_newline":
                chat_box.insert("\n")
                return False  # Cancels default behavior

        # Let all other actions and focus states pass through normally
        return True


    def action_submit_message(self) -> None:
        chat = self.query_one("#chat-container", VerticalScroll)
        input_box = self.query_one("#input", TextArea)

        user_input = input_box.text.strip()
        if not user_input:
            return
        if user_input == "":
            np_audio = audio_recorder.record_until_enter_key_pressed()
            np_audio = np_audio.squeeze()
            stt_generator.config["audio"] = np_audio
            output = stt_generator.generate()
            user_input = " ".join([artifact.data for artifact in output.batch])
            print(user_input)
        payload = {
            "conversation_id": "test1234", 
            "content": user_input
        }
        chat.mount(Static(f"[bold #FF13F0]You:[/]"))
        chat.mount(ChatMessage(user_input + "\n"))

        response = orchestrator.process(payload)

        chat.mount(Static(f"[bold cyan]{orchestrator.bot.config["name"]}[/]: "))
        chat.mount(ChatMessage(response + "\n"))

        input_box.text = ""
        chat.scroll_end(animate=False)


    def load_stt_generator(self):
        if "stt" not in self.config:
            return
        stt_generator = registry.get_model_class(
            self.config["stt"]
        )
        stt_generator.load()
        if "warmup" in self.config["stt"]:
            if self.config["stt"]["warmup"]:
                stt_generator.warmup()
        return stt_generator

    
    def load_audio_recorder(self):
        if "audio_recorder" not in self.config:
            return
        audio_recorder = AudioRecorder(self.config["audio_recorder"])
        return audio_recorder



if __name__ == "__main__":
    ChatApp(
        orchestrator=orchestrator,
        interface_config=interface_config
    ).run()
