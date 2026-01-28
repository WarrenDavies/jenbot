import textwrap


class ResponseGenerator:

    def create_tool_use_prompt(self, tool_response):
        content = f"""
        TOOL USE RESULT 
        Tool name: {tool_response["name"]}
        Status: {tool_response["status"]} 
        Output: {tool_response["output"]}
        
        Add the tool output to your response in a natural way to answer the user's previous query."""
        content = textwrap.dedent(content)

        system_prompt = {"role": "system", "content": content}

        return system_prompt


    def generate(self, message, tool_response = None):

        if tool_response:
            tool_use_prompt = self.create_tool_use_prompt(tool_response)
            message["messages"].append(tool_use_prompt)
        
        return message
