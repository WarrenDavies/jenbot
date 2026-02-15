from abc import ABC, abstractmethod
import textwrap
import datetime

from speechjenerator.registry import get_model_class

from textjenerator import registry


class BaseBot(ABC):

    def __init__(self, config):
        self.config = config
        self.load_generator()
        self.speech_generator = self.setup_tts()

    
    def setup_tts(self):

        if "tts" in self.config:
            tts_model = get_model_class(self.config["tts"]["generator_config"])
            return tts_model

        return None
        

    def speak(self, text):
        if "tts" not in self.config:
            return

        self.speech_generator.config["text"] = text
        output = self.speech_generator.generate()
        speech = output.batch[0]
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        speech.play(self.config["tts"]["output_path"] + "/" + ts + speech.extension)


    def load_generator(self):
        self.generator = registry.get_model_class(self.config["generator_config"])
        self.generator.load()

    
    def create_tool_use_prompt(self, tool_response, message):
        content = f"""TOOL USE RESULT 
        Tool name: {tool_response["name"]}
        Tool description: {tool_response["description"]}
        Status: {tool_response["status"]} 
        Output: {tool_response["output"]}
                
        Include the details of the tool use in your response in a natural way to answer the user's previous query."""
        
        content_stripped = [line.lstrip() for line in content.splitlines()]
        content = '\n'.join(content_stripped)
        content = textwrap.dedent(content)

        tool_use_system_prompt = {
            "role": "system", 
            "content": content,
            "conversation_id": message["conversation_id"]
        }

        return tool_use_system_prompt


    @abstractmethod
    def generate():
        pass
