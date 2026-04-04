import textwrap

from jenerationutils.storage.storage_manager import StorageManager

from jenbot.storage.record_manager import RecordManager
from jenbot.core.intent_parser import IntentParser
from jenbot.tools.toolkit import Toolkit
from jenbot.chat.response_generator import ResponseGenerator
from jenbot.schemas.registry import REGISTRY as schema_registry

from jenbot.bots.roastbot.roastbot import Roastbot
from jenbot.bots.jenbot.jenbot import Jenbot
from jenbot.bots.interview_bot import InterviewBot


class Orchestrator():
    """
    Manages the sequences of events, and the data flow, through the system.
    """
    def __init__(self, config):
        """
        Initialises the orchestrator.
        """
        self.intent_parser = IntentParser(config=config["router"])
        self.storage_manager = StorageManager(config, schema_registry=schema_registry)
        self.record_manager = RecordManager(self.storage_manager, config)
        self.toolkit = Toolkit()
        self.bot = InterviewBot(config["bot"], self.storage_manager, self.record_manager)


    def save_record(self, data, dataset_name):
        record, primary_key = self.record_manager.create_record(
            data,
            dataset_name
        )
        self.storage_manager.data_connection.append_data(dataset_name, record)
        return primary_key


    def process(self, message):
        message["role"] = "user"
        message_id = self.save_record(message, "messages")

        intent = self.intent_parser.get_intent(message["content"])
        intent["message_id"] = message_id
        intent_id = self.save_record(intent, "intent")

        tool_response = self.toolkit.use_tool(intent)
        if tool_response:
            tool_response_system_prompt = self.bot.create_tool_use_prompt(
                tool_response, message
            )
            self.save_record(tool_response_system_prompt, "messages")

        response = self.bot.generate(message)
        self.save_record(response, "messages")

        self.bot.speak(response["content"])

        return response["content"]
   