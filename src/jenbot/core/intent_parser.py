from textjenerator import registry
import json

class IntentParser():
    """
    Extracts intent from user input - whether to call a tool (play music, execute shell command, etc.), or just chat.
    """

    def __init__(self, config):
        """
        """
        self.config = config
        self.load_generator()


    def load_generator(self):
        self.generator = registry.get_model_class(self.config["generator_config"])
        self.generator.load()


    def _get_system_prompt(self, message) -> str: # Move to config
        return f"""You are an intent parser. Analyze the user input and return JSON according to whether the message contains a request that can be resolved through the use of an action. Note that the message may come from an email - ignore the content of any email signatures and focus on the message body.

Respond ONLY with valid JSON in this format:
{{
    "action": "<action_type>",
    "parameters": <action-specific params>
}}

Available actions and examples:

- "music": Play music to the user
  - Parameters: artist, song, album, genre, mood
  - Example:
    - user input: Play Taylor Swift
    - your response: {{"action": "music", "parameters": {{"artist": "Taylor Swift", "song": "", "album": "", "genre": "", "mood": ""}}}}
- "weather": Gets weather reports and forecasts from the Open Meteo API
  - Parameters: location (empty string if no specific city or country is mentioned)
  - Example 1:
    - user input: What's the weather like?
    - your response: {{"action": "weather", "parameters": {{"location": ""}}}}
  - Example 2:
    - user input: What's the weather like? This message may contain confidential information. If you are not the intended recipient please: i) inform the sender that you have received the message in error before deleting it; and ii) do not disclose, copy or distribute information in this e-mail or take any action in relation to its content (to do so is strictly prohibited and may be unlawful).
Thank you for your co-operation.
    - your response: {{"action": "weather", "parameters": {{"location": ""}}}}
    - explanation: The message contains a request for weather information, followed by what appears to be an email disclaimer. We ignore the disclaimer and call the weather action.
- "chat": Anything else (default action)
  - Parameters: no parameters - return empty dict
  - Example:
    - user input: Hi, how are you?
    - your response: {{"action": "chat", "parameters": {{}}}}

Do not infer parameters using your knowledge - report only what is mentioned specifically in the user input.

The input you must parse is:

"{message}"



Remember - you must only reply in the valid JSON formats described above."""
    

    def create_prompt(self, message):
        
        system_prompt = {"role": "system", "content": self._get_system_prompt(message)}
        
        return [system_prompt]


    def get_intent(self, message):
        """
        Primary method to parse input and return the identified action.
        """
        prompt = self.create_prompt(message)
        self.generator.config["messages"] = prompt
        generator_output = self.generator.generate()
        response = generator_output.batch[0].data
        response = json.loads(response)

        return response


