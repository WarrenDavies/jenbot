import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from jenbot.schemas.registry import register

@register("intent")
class IntentSchema(BaseModel):
    intent_id: str = ""
    message_id: str = ""
    action: str = ""
    parameters: Dict[str, Any] = {}

    @staticmethod
    def get_primary_key_name():
        return "intent_id"


    