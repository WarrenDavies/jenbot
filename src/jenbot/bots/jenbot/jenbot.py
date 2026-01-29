from abc import ABC, abstractmethod
import textwrap

from jenbot.bots.base.base_bot import BaseBot


class Jenbot(BaseBot):


    def __init__(self, config):
        super().__init__(config)
        self.config = config

    
    def generate(self, prompt):

        reponse = "beep beep boop boop I'm replying"
        
        return {
            "role": "assistant",
            "content": reponse
        }
