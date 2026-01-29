from abc import ABC, abstractmethod
import textwrap


class BaseBot(ABC):

    def __init__(self, config):
        self.config = config

    
    def create_tool_use_prompt(self, tool_response):
        content = f"""TOOL USE RESULT 
        Tool name: {tool_response["name"]}
        Status: {tool_response["status"]} 
        Output: {tool_response["output"]}
                
        Include the details of the tool use in your response in a natural way to answer the user's previous query."""
        
        content_stripped = [line.lstrip() for line in content.splitlines()]
        content = '\n'.join(content_stripped)
        content = textwrap.dedent(content)

        tool_use_system_prompt = {"role": "system", "content": content}

        return tool_use_system_prompt


    @abstractmethod
    def generate():

        pass
