


class IntentParser():
    """
    Extracts intent from user input - whether to call a tool (play music, execute shell command, etc.), or just chat.
    """

    def __init__(self, config):
        """
        """
        self.config = config
        self.generator = None # text_jenerator would be instantiated here
        self.system_prompt = self._get_system_prompt()


    def _get_system_prompt(self) -> str: # Move to config
        return """You are an intent parser. Analyze the user input and return JSON.

Available actions:
- "music": Play music. Extract artist, song, genre if mentioned.
- "image": Generate image. Extract the visual description.
- "chat": General conversation (default fallback).

Respond ONLY with valid JSON in this format:
{
    "action": "<action_type>",
    "confidence": <0.0-1.0>,
    "parameters": {<action-specific params>}
}

Examples:
User: "Play some Taylor Swift"
{"action": "music", "confidence": 0.95, "parameters": {"artist": "Taylor Swift"}}

User: "What's the weather like?"
{"action": "chat", "confidence": 0.9, "parameters": {"message": "What's the weather like?"}}

User: "Show me disk usage"
{"action": "shell", "confidence": 0.85, "parameters": {"intent": "display disk usage", "suggested_command": "df -h"}}"""
    

    def get_action(self, message):
        """
        Primary method to parse input and return the identified action.
        """
        last_message = message["messages"][-1]["content"]

        if "weather" in last_message:
            intent = {
                "action": "weather",
                "parameters": {
                    "location": "London"
                }
            }
        else:
            intent = {
                "action": "None",
                "parameters": {}
            }

        return intent


