import textwrap

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


    def use_tool(self, intent):
        tool_response = None
        if intent["action"] and (intent["action"] in tools_registry.get_tools_list()):
            ToolClass = tools_registry.get_class(intent["action"])
            tool = ToolClass()
            tool_response = tool.run(intent["parameters"])
        return tool_response


    def process(self, message):
        intent = self.intent_parser.get_action(message)
        tool_response = self.use_tool(intent)
        response = self.response_generator.generate(message, tool_response)

        return response


    