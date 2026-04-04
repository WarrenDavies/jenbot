from abc import ABC, abstractmethod
import textwrap
import csv
import datetime
import random
import time

from speechjenerator.registry import get_model_class

from jenbot.bots.base.base_bot import BaseBot
from jenbot.memory.memory_manager import MemoryManager


class InterviewBot(BaseBot):


    def __init__(self, config, storage_manager, record_manager):
        super().__init__(config)
        self.storage_manager = storage_manager
        self.record_manager = record_manager
        self.memory_manager = MemoryManager(config["memory"], storage_manager, record_manager)
        self.memory_config = {}
        self.competencies = self.select_competencies()
        self.current_question = None


    def save_record(self, data, dataset_name):
        record, primary_key = self.record_manager.create_record(
            data,
            dataset_name
        )
        self.storage_manager.data_connection.append_data(dataset_name, record)
        return primary_key


    def _get_system_prompt(self) -> str:
        return {
            "role": "system",
            "content": f"""You are {self.config["interviewer"]["name"]}, {self.config["interviewer"]["interviewer_role"]} at {self.config["interviewer"]["organisation"]}. You are conducting a multi-turn competency-based interview for the role of {self.config["interviewer"]["vacancy"]}.
            
            RULES:
            1. Always act as the interviewer. When the conversation first begins, greet the applicant.
            2. Your first message must be a single competency-based interview question derived from the given competency. The question should start with 'Give me an example of a time when...' or similar.
            3. After the applicant responds, assess whether their answer demonstrates the competency:
            - Did their answer actually address the question?
            - Was it a specific example, rather than a general answer?
            - Did they provide enough detail and demonstrate skill/knowledge?
            - Was anything missing or unclear?
            4. Ask 0-3 follow-up questions to probe or clarify.
            5. Only after all follow-up questions are exhausted, reply with exactly: NEXT QUESTION
            6. Never summarize the applicant's answers. Never provide guidance or tips. Stick to asking questions only.

            You will always be provided with a competency. Generate your questions strictly based on the provided competency."""
        }


    def select_competencies(self):
        config_competencies = self.config["interviewer"]["competencies"]

        competencies = []
        for competency, sub_competencies in config_competencies.items():
            question_config = {}
            question_config["competency"] = competency
            question_config["sub-competency"] = random.choice(sub_competencies)
            question_config["status"] = "unasked"
            competencies.append(question_config)
        return competencies


    def get_unasked_question_indices(self):
        return [
            i for i, competency in enumerate(self.competencies) 
            if competency["status"] == "unasked"
        ]


    def create_question(self, message):
        question = {
            "role": "system",
            "content": self.create_question_prompt(),
            "conversation_id": message["conversation_id"]
        }
        return question


    def create_question_prompt(self):
        
        question_prompt = f"""Here is the competency for your next question:

        {self.competencies[self.current_question]["sub-competency"]}

        Generate one clear, specific, competency-based interview question based on this. Start with 'Give me an example of a time when...' or similar. No extra text, no acknowledgments.
        """
        return question_prompt


    def get_last_n_records(self, csv_file_path, n):
        last_n_records = []

        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                last_n_records.append({"role": row.get("role", ""), "content": row.get("content", "")})
                if len(last_n_records) > n:
                    last_n_records.pop(0)

        return last_n_records


    def mark_current_question_asked(self):
        self.competencies[self.current_question]["status"] = "asked"

 

    def generate(self, message):
        prompt = [self._get_system_prompt()]

        if self.current_question == None:
            unasked_question_indices = self.get_unasked_question_indices()
            self.current_question = random.choice(unasked_question_indices)
            self.save_record(self.create_question(message), "messages")

        recent_messages = self.memory_manager.get_recent_messages(message["conversation_id"])

        prompt.extend(recent_messages)

        self.generator.config["messages"] = prompt
        generator_output = self.generator.generate()
        response = generator_output.batch[0].data

        if "NEXT QUESTION" in response:
            self.mark_current_question_asked()
            unasked_question_indices = self.get_unasked_question_indices()
            self.current_question = random.choice(unasked_question_indices)
            self.save_record(self.create_question(message), "messages")

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
