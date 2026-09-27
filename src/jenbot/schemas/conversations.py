from pydantic import BaseModel, Field

from jenbot.schemas.registry import register

@register("conversations")
class ConversationsSchema(BaseModel):
    conversation_id: str = ""
    conversation_title: str = ""
    title_source: str = ""
    created_time: str = ""
    updated_time: str = ""
    tags: str = ""

    @staticmethod
    def get_primary_key_name():
        return "conversation_id"
