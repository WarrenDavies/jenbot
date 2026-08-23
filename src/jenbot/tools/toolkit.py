from jenbot.tools import registry as tools_registry

class Toolkit():

    def __init__(self, config):
        self.config = config
        self.tools = self.initialise_tools()


    def initialise_tools(self):
        tools = {}
        for tool_name, tool_config in self.config.items():
            ToolClass = tools_registry.get_class(tool_name)
            tool_object = ToolClass(tool_config)
            tools[tool_name] = tool_object
        return tools


    def use_tool(self, intent):
        if "action" not in intent:
            return None
        tool_requested = intent["action"]
        if tool_requested and (tool_requested in self.tools):
            tool_params = intent
            tool_response = self.tools[tool_requested].run(tool_params)
            return tool_response
        