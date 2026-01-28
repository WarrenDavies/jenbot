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
        self.record_manager = RecordManager(config)

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


    def save_record(self, data, dataset_name):
        data_row = self.record_manager.create_record(
            data,
            dataset_name,
            self.storage_manager
        )
        self.storage_manager.data_connections["messages"].append_data(data_row)

    def process(self, message):
        # save the incoming message
        message["role"] = "user"
        self.save_record(message, "messages")

        intent = self.intent_parser.get_action(message["content"])
        ## TODO: (later) Save decision on intent to decisions table here

        tool_response = self.use_tool(intent) # TODO: (now) Create Toolkit class
        ## TODO: (later) Save tool response to table here



        response = self.response_generator.generate(message, tool_response)
        ## TODO: (now) Save assistant message to messages table here

        return response
   