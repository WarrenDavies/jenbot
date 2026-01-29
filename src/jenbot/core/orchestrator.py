import textwrap

from jenerationutils.storage.storage_manager import StorageManager

from jenbot.storage.record_manager import RecordManager
from jenbot.core.intent_parser import IntentParser
from jenbot.tools.toolkit import Toolkit
from jenbot.chat.response_generator import ResponseGenerator

from jenbot.bots.jenbot.jenbot import Jenbot

class Orchestrator():
    """
    Manages the sequences of events, and the data flow, through the system.
    """
    def __init__(self, config):
        """
        Initialises the orchestrator.
        """
        self.intent_parser = IntentParser(config=None)
        self.response_generator = ResponseGenerator()
        self.storage_manager = StorageManager(config)
        self.record_manager = RecordManager(self.storage_manager, config)
        self.toolkit = Toolkit()
        self.bot = Jenbot(config["bot"])


    def process(self, message):
        message["role"] = "user"
        message_id = self.record_manager.save_record(message, "messages")

        intent = self.intent_parser.get_action(message["content"])
        intent["message_id"] = message_id
        intent_id = self.record_manager.save_record(intent, "intent")

        tool_response = self.toolkit.use_tool(intent)
        if tool_response:
            tool_response_system_prompt = self.bot.create_tool_use_prompt(
                tool_response
            )
            self.record_manager.save_record(tool_response_system_prompt, "messages")

        response = self.bot.generate(message)

        self.record_manager.save_record(response, "messages")

        return response["content"]
   