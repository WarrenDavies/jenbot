from abc import ABC, abstractmethod
import textwrap
import csv
import datetime
import random

from speechjenerator.registry import get_model_class

from jenbot.bots.base.base_bot import BaseBot
from jenbot.memory.memory_manager import MemoryManager


class InterviewBot(BaseBot):


    def __init__(self, config, storage_manager, record_manager):
        super().__init__(config)
        self.memory_manager = MemoryManager(config["memory"], storage_manager, record_manager)
        self.memory_config = {}
        self.competencies = self.select_competencies()


    def _get_system_prompt(self) -> str:
        return {
            "role": "system",
            "content": f"""You are {config["interviewer"]["name"]}, {config["interviewer"]["interviewer_role"]} at {config["interviewer"]["organisation"]}. You are conducting a competency - based interview for the role of {config["interviewer"]["vacancy"]}."""
        }


    def select_competencies(self):
        config_competencies = self.config["interviewer"]["competencies"]

        competencies = {}
        for competency, sub_competencies in config_competencies.items():
            competencies[competency] = random.choice(sub_competencies)

        return competencies


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
