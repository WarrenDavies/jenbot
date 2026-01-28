from jenbot.tools import registry as tools_registry

class Toolkit():
    def use_tool(self, intent):
        tool_response = None
        if intent["action"] and (intent["action"] in tools_registry.get_tools_list()):
            ToolClass = tools_registry.get_class(intent["action"])
            tool = ToolClass()
            tool_response = tool.run(intent["parameters"])
        return tool_response