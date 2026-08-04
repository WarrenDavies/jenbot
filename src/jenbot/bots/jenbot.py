from abc import ABC, abstractmethod
import textwrap
import csv
import datetime


from speechjenerator.registry import get_model_class

from jenbot.bots.base_bot import BaseBot
from jenbot.memory.memory_manager import MemoryManager
from jenbot.bots.registry import register


@register("jenbot")
class Jenbot(BaseBot):


    def __init__(self, config, storage_manager, record_manager):
        super().__init__(config)
        self.memory_manager = MemoryManager(config["memory"], storage_manager, record_manager)
        self.memory_config = {}


    def _get_system_prompt(self) -> str:
        return {
            "role": "system",
            "content": """You are Jenbot, an expert, helpful, and diligent assistant.

You provide the user with accurate answers to their queries. You are polite, friendly, and a little sarcastic.

You have access to the following tools:
* Weather - gets the current weather by accessing the Meteo API

You can tell the user about these tools, but the user will have to request them before you can use them, you can't call them yourself directly.
"""
        }

    def get_last_n_records(self, csv_file_path, n):
        last_n_records = []

        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                last_n_records.append({"role": row.get("role", ""), "content": row.get("content", "")})
                if len(last_n_records) > n:
                    last_n_records.pop(0)

        return last_n_records

 
    def generate(self, message):
        prompt = [self._get_system_prompt()]

        recent_messages = self.memory_manager.get_recent_messages(message["conversation_id"])

        prompt.extend(recent_messages)

        self.generator.config["messages"] = prompt
        generator_output = self.generator.generate()
        response = generator_output.batch[0].data

        return {
            "role": "assistant",
            "conversation_id": message["conversation_id"],
            "bot": self.config["name"],
            "content": response,
        }
