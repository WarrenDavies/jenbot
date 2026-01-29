from abc import ABC, abstractmethod
import textwrap
import csv

from jenbot.bots.base.base_bot import BaseBot


class Jenbot(BaseBot):


    def __init__(self, config):
        super().__init__(config)


    def get_last_two_records(self, csv_file_path):
        # Initialize a list to store the last two records
        last_two_records = []

        # Open the CSV file and read the last two rows
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            # Create a CSV reader object
            csv_reader = csv.DictReader(file)

            # Iterate through the CSV rows and collect the last two
            for row in csv_reader:
                last_two_records.append({"role": row.get("role", ""), "content": row.get("content", "")})
                # Keep only the last two records
                if len(last_two_records) > 2:
                    last_two_records.pop(0)

        return last_two_records

    
    def generate(self, prompt):

        prompt = self.get_last_two_records("./data/messages.csv")
        self.generator.config["messages"] = prompt
        generator_output = self.generator.generate()
        reponse = generator_output.batch[0].data

        return {
            "role": "assistant",
            "content": reponse
        }
