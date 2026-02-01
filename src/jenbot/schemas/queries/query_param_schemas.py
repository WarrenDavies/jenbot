import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

# from jenbot.schemas.registry import register

# @register("messages")
class GetRecentMessages(BaseModel):
    conversation_id: str = "Test"
    number_of_messages: int = 5
