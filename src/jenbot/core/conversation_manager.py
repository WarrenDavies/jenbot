import random
import datetime
import uuid

from jenbot.utils import time_as_words
from jenbot.schemas.conversations import ConversationsSchema
from jenbot.storage import queries

FIRST_WORD = [
"New", "Latest", "Another", "Just another", "One more", "Fresh", "Quick", "Rainy-day", "Sunny", "Cosy", "Big", "Little", "Random", "Spontaneous", "Impromptu", "Unplanned", "Deep", "Casual", "Serious", "Curious", "Wandering", "Fascinating", "Incredible", "Necessary", "Next", "Important", "Cool", "Extraordinary", "Productive", "The Great", "Mildly Interesting", "SEGMENT_OF_DAY", "DAY_OF_WEEK", "DAY_OF_WEEK_AND_SEGMENT_OF_DAY", "MONTH", "SEGMENT_OF_WEEK"]

SECOND_WORD = [ "Conversation", "Chat", "Chit chat", "Parlay", "Chin wag", "Natter", "Yarn", "Jaw", "Talk", "Discussion", "Huddle", "Powwow", "Sit-down", "Confab", "Rundown", "Tête-à-tête", "Catch-up", "Debrief", "Brainstorm", "Session", "Thread", "Chat", "Blather", "Gab", "Gossip", "Banter", "Rabbit hole", "Tangent", "Detour", "Ramble", "Deep dive", "Brainwave", "Musings", "Ponder", "Pontifications", "Hot take", "Soapbox", "Symposium", "Roundtable", "Jamboree", "Gathering", "Meetup", "Hangout", "Hootenanny", "Kaffeeklatsch", "Coffee break", "Bull session", "Shooting of the breeze", "Free-for-all", "Q&A", "Mull", "Rumination", "Jam session", "Adventure", "Shenanigans", "Escapade", "Investigation", "Exploration", "Kerfuffle",  "Endeavour"]


class ConversationManager():

    def __init__(record_manager):
        self.record_manager = record_manager
        pass


    def get_recent_messages(
        self,
        conversation_id,
        number_of_messages = None
    ):
        """
        Get `number_of_messages` messages from the conversation
        with the specified, `conversation_id`
        (now)
        """

        if number_of_messages is None:
            number_of_messages = self.config.get(
                "max_messages_in_context",
                10
            )

        values = (conversation_id, number_of_messages)
        query = queries.get_recent_messages()
        
        query_result = self.storage_manager.data_connection.execute(query, values)

        return query_result


    def get_conversation_ids(
        self,
    ):
        query = queries.get_conversation_ids()

        query_result = self.storage_manager.data_connection.execute(query)

        return query_result


    @staticmethod
    def create_conversation_title():
        first_word = random.choice(FIRST_WORD)
        if first_word in time_as_words.word_creator_registry:
            get_word = time_as_words.word_creator_registry[first_word]
            first_word = get_word(datetime.datetime.now())
        second_word = random.choice(SECOND_WORD)

        return first_word + " " + second_word


    def create_conversation(self, title=None):
        if not title:
            title = self.create_conversation_title()
            source = "auto"
        else:
            source = "user"

        conversation_record = {
            "conversation_title": title,
            "title_source": source,
            "updated_time": "",
            "tags": ""
        }
        conversation_record_enriched, primary_key_value = (
            self.record_manager.create_record(conversation_record, "conversations")
        )
        self.storage_manager.data_connection.append_data(
            "conversations", 
            conversation_record_enriched
        )
        return {
            conversation_id: primary_key_value,
            title: title
        }

    def rename_conversation(self):
        pass


    def delete_conversation(self):
        pass

    
    def update_conversation_metadata(self):
        pass
