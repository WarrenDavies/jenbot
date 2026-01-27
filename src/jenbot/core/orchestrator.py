from jenbot.core.intent_parser import IntentParser


class Orchestrator():
    """
    Manages the sequences of events, and the data flow, through the system.
    """


    def __init__(self, config):
        """
        Initialises the orchestrator.
        """
        self.intent_parser = IntentParser(config=None)
    
    def handle_input(self, message):
        action = self.intent_parser.get_action(message)
        return action


    