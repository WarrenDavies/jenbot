from abc import ABC, abstractmethod
import textwrap
import csv

from jenbot.bots.base.base_bot import BaseBot


class Jenbot(BaseBot):


    def __init__(self, config):
        super().__init__(config)
        self.messages_to_keep_in_context = 6


    def _get_system_prompt(self) -> str:
        return {
            "role": "system",
            "content": """You are Jenbot, an expert, helpful, and diligent assistant.

You provide the user with accurate answers to their queries. You are polite, friendly, and a little sarcastic.

You have access to the following tools:
* Weather - gets the current weather by accessing the Meteo API
* Music - plays music on the user's computer

When you have used a tool, the result will be available to you in a "system" message labelled TOOL_USE_RESULT. You should incorporate this information into your response to the user.
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

 
    def generate(self, prompt):
        prompt = [self._get_system_prompt()]
        prompt.extend(
            self.get_last_n_records(
                "./data/messages.csv",
                self.messages_to_keep_in_context
            )
        )
        self.generator.config["messages"] = prompt
        generator_output = self.generator.generate()
        response = generator_output.batch[0].data

        return {
            "role": "assistant",
            "bot": self.config["name"],
            "content": response,
        }
