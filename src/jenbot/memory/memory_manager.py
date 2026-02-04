from pydantic import BaseModel

from jenbot.storage import queries


class MemoryManager():

    def __init__(self, config, storage_manager, record_manager):
        self.config = config
        self.storage_manager = storage_manager
        self.record_manager = record_manager


    def get_recent_messages(
        self,
        conversation_id
    ):
        """
        Get `number_of_messages` messages from the conversation
        with the specified, `conversation_id`
        (now)
        """

        values = (conversation_id, self.config["max_messages_in_context"])
        query = queries.get_recent_messages()
        
        query_result = self.storage_manager.data_connection.execute(query, values)

        return query_result


    def retrieve_conversation_summaries(
        self, 
        number_of_messages, 
        working_memory_ruleset
    ):
        """
        Retrieve stored summaries of older messages as indicated by 
        the `working_memory_ruleset`.
        (later)
        """
        pass


    def get_relevant_messages_from_all_conversation(self):
        """
        Get relevant messages from other conversations using RAG,
        a tagging system, or some other method. 
        (later)
        """
        pass


    def should_remember_this(self, memorisation_ruleset) -> bool:
        """
        Parse user input and decide whethere it contains anything that should be added to the bot's memory (e.g., to store preferences and other useful knowledge".).

        The `memorisation_ruleset` contains parameters that influence
        this decision.
        (later)
        """
        pass


    def store_memory(self):
        """
        Save a memory (Not a full message sent by the user, but a piece
        of information identified as being worth remembering).
        (later)
        """
        pass


    def retrieve_memory(self, working_memory_ruleset):
        """
        Retrieve relevant stored memories, as determined by the 
        `working_memory_ruleset` (e.g, confidence score, number to return,
        etc.).
        (later)
        """
        pass


    
