import textwrap

from jenerationutils.storage.storage_manager import StorageManager

from jenbot.storage.record_manager import RecordManager
from jenbot.core.intent_parser import IntentParser
from jenbot.tools import registry as tools_registry
from jenbot.chat.response_generator import ResponseGenerator


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


    def use_tool(self, intent):
        ### TODO: Move to its own class
        tool_response = None
        if intent["action"] and (intent["action"] in tools_registry.get_tools_list()):
            ToolClass = tools_registry.get_class(intent["action"])
            tool = ToolClass()
            tool_response = tool.run(intent["parameters"])
        return tool_response


    def flag_role(self, message, role):
        message["role"] = role
        return message


    def process(self, message):
        message["role"] = "user"
        self.record_manager.save_record(message, "messages")
        intent = self.intent_parser.get_action(message["content"])

        tool_response = self.use_tool(intent) # TODO: (now) Create Toolkit class
        if tool_response:
            tool_response_system_prompt = self.response_generator.create_tool_use_prompt(
                tool_response
            )
            self.record_manager.save_record(tool_response_system_prompt, "messages")

        response = self.response_generator.generate(message)
        self.record_manager.save_record(response, "messages")

        return response
   