import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from jenbot.schemas.registry import register

@register("messages")
class MessagesSchema(BaseModel):
    message_id: str = ""
    conversation_id: str = "Test"
    record_created_time: str = ""
    role: str = ""
    content: str = ""
    bot: str = ""

    @staticmethod
    def get_primary_key_name():
        return "message_id"


    