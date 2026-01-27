import textwrap

from jenbot.core.intent_parser import IntentParser


class WeatherTool:
    def __init__(self):
        self.name = "weather"
    def run(self, parameters):
        return {
            "name": self.name,
            "status": "success",
            "output": f"The weather outside is frightful, but the fire is so delightful"
        }

tools_registry = {
    "weather": WeatherTool
}


class Chat:
    def generate_response(self, messages, tool_response = None):
        chat_response = f"""
        The message sent was: {messages}
        TOOL_RESPONSE
        """

        if tool_response:
            tool_response_replacement = f"""
            You used the {tool_response["name"]} tool for the user. 
            The tool request status was: {tool_response["status"]}. 
            The tool output was {tool_response["output"]}"""
        else: 
            tool_response_replacement = ""
        
        chat_response = chat_response.replace(
            "TOOL_RESPONSE",
            tool_response_replacement
        )

        chat_response = textwrap.dedent(chat_response)

        return chat_response


class Orchestrator():
    """
    Manages the sequences of events, and the data flow, through the system.
    """
    def __init__(self, config):
        """
        Initialises the orchestrator.
        """
        self.intent_parser = IntentParser(config=None)
        self.chat = Chat()


    def use_tool(self, intent):
        tool_response = None
        if intent["action"] and (intent["action"] in tools_registry.keys()):
            ToolClass = tools_registry[intent["action"]]
            tool = ToolClass()
            tool_response = tool.run(intent["parameters"])
        return tool_response


    def process(self, message):
        intent = self.intent_parser.get_action(message)
        tool_response = self.use_tool(intent)
        response = self.chat.generate_response(message, tool_response)

        return response


    