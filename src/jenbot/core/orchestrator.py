import textwrap
import uuid
import json

from jenerationutils.storage.storage_manager import StorageManager

from jenbot.storage.record_manager import RecordManager
from jenbot.core.intent_parser import IntentParser
from jenbot.tools.toolkit import Toolkit
from jenbot.chat.response_generator import ResponseGenerator
from jenbot.schemas.registry import REGISTRY as schema_registry

from jenbot.bots.roastbot.roastbot import Roastbot
from jenbot.bots.jenbot.jenbot import Jenbot
from jenbot.bots.interview_bot import InterviewBot


class Orchestrator():
    """
    Manages the sequences of events, and the data flow, through the system.
    """
    def __init__(self, config):
        """
        Initialises the orchestrator.
        """
        self.intent_parser = IntentParser(config=config["router"])
        self.storage_manager = StorageManager(config, schema_registry=schema_registry)
        self.record_manager = RecordManager(self.storage_manager, config)
        self.toolkit = Toolkit()
        self.bot = Jenbot(config["bot"], self.storage_manager, self.record_manager)


    def save_record(self, data, dataset_name):
        record, primary_key = self.record_manager.create_record(
            data,
            dataset_name
        )
        self.storage_manager.data_connection.append_data(dataset_name, record)
        return primary_key


    def process(self, message):

        message["role"] = "user"
        message_id = self.save_record(message, "messages")

        intent = self.intent_parser.get_intent(message["content"])
        intent["message_id"] = message_id
        intent_id = self.save_record(intent, "intent")

        tool_response = self.toolkit.use_tool(intent)
        if tool_response:
            tool_response_system_prompt = self.bot.create_tool_use_prompt(
                tool_response, message
            )
            self.save_record(tool_response_system_prompt, "messages")

        response = self.bot.generate(message)
        self.save_record(response, "messages")

        self.bot.speak(response["content"])

        return response["content"]


    def process_ambient_mode(self):
        
        while True:
            if self.bot.status == "waiting":
                message = self.bot._get_ambient_mode_prompt()
                message["role"] = "system"
                message["conversation_id"] = "ambient"
                print("system:", message)
                message_id = self.save_record(message, "messages")
                self.bot.status = "responding"
                
            response = self.bot.generate(message)
            print("Jenbot:", response["content"])
            try:
                action_dict = json.loads(response["content"])
                print("  json loaded")
                action = action_dict["action"]
                print("  action extracted")
            except:
                action = response["content"]
            print("action found: ", action)
            assistant_message = {
                "role": "assistant",
                "content": action,
                "conversation_id": "ambient",
            }
            message_id = self.save_record(assistant_message, "messages")
            print("available Actions: ", self.bot.ambient_mode_actions.keys())
            if action in self.bot.ambient_mode_actions.keys():
                if action == "skip":
                    skip_message = {
                        "role": "assistant",
                        "content": "skip",
                        "conversation_id": "ambient",                
                    }
                    self.save_record(skip_message, "messages")   
                    exit_message = {
                        "role": "system",
                        "content": "Skip message received: exiting.",
                        "conversation_id": "ambient",                
                    }
                    self.save_record(exit_message, "messages")
                    print("System:", exit_message["content"])
                    self.bot.mode = "ambient"
                    self.bot.status = "waiting"
                    conversation_id = "ambient"
                    return conversation_id

                if action == "message_user":

                    # switch bot mode
                    self.bot.mode = "chat"
                    self.bot.status = "active"

                    # create new conversation
                    new_conversation_id = uuid.uuid4().hex[:8]

                    # create prompt
                    message_user_message = {
                        "role": "system",
                        "content": "System message: You have chosen to message the user, you are now exiting ambient mode and initiating a chat session with the user. Respond with the message you want to send them. Reply in plain text (no JSON needed here!)",
                        "conversation_id": "ambient",                
                    }
                    self.save_record(message_user_message, "messages")
                    print("system: ", message_user_message["content"])

                    # get recent messages from ambient mode
                    recent_ambient_messages = self.bot.memory_manager.get_recent_messages("ambient")
                    recent_ambient_messages.append({
                        "role": "assistant",
                        "content": message_user_message["content"],
                    })
                    # Save recent ambient message history to new conversation
                    for recent_ambient_message in recent_ambient_messages:
                        recent_ambient_message["conversation_id"] = new_conversation_id
                        self.save_record(recent_ambient_message, "messages")
                    
                    message_user_message["conversation_id"] = new_conversation_id
                    response = self.bot.generate(message_user_message)
                    print(response["content"])
                    self.save_record(response, "messages")
                    self.bot.speak(response["content"])
                    return new_conversation_id

                intent = {
                    "action": self.bot.ambient_mode_actions[action],
                    "parameters": {}
                }
                tool_response = self.toolkit.use_tool(intent)
                print(tool_response)
                tool_response_system_prompt = self.bot.create_tool_use_prompt(
                    tool_response, {"conversation_id": "ambient"}
                )
                print(tool_response_system_prompt)
                self.save_record(tool_response_system_prompt, "messages")

            else:
                input_not_recognised_message = {
                    "role": "system",
                    "content": f"""System message to Jenbot: Response not recognised. Please ensure your response is ONLY json in this format:

{{"action": <name_of_action>}}

Available action names:
{self.bot.ambient_mode_actions_prompt}

It has to be ONLY the JSON, without code fences or any other text or acknowledgement.

                    """,
                    "conversation_id": "ambient",                
                }
                print(input_not_recognised_message["content"])
                self.save_record(input_not_recognised_message, "messages")   
                