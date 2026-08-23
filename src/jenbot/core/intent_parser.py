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
- "image": Generates an image using a diffusion model. 
  - Parameters: prompt: You must convert the user input into a prompt that can be passed to a diffusion model, and include this prompt in your JSON response. If the user input is very short such as just "a cat", "a boat", "a person", and does not specify a style or other details, please add extra details yourself.
  - Example 1:
    - user input: OK yes please make an image of a samurai in a rainy cyberpunk street
    - your response: {{"action": "image", "parameters": {{"prompt": samurai, cyberpunk aesthetic, city street, neon lights, rainy, puddles, with reflections of neon""}}}}
  - Example 2:
    - user input: Oh yes I love chocolate. Make an image of a bowl of fruit in the style of an oil painting
    - your response: {{"action": "image", "parameters": {{"prompt": bowl of fruit, oil painting style""}}}}
    - explanation: the "Oh yes I love chocolate" part is not part of the image generation request so it was not included in the prompt.
  - Example 3:
    - user input: Make an image of a cat
    - your response: {{"action": "image", "parameters": {{"prompt": an orange cat, sitting on a windowsill, cartoon style""}}}}
    - explanation: The request did not specify any details other than 'a cat'. In cases like this, please add additional detail yourself."
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
        print(response)
        response = json.loads(response)

        return response


