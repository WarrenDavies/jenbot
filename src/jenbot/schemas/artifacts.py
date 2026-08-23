import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from jenbot.schemas.registry import register


@register("artifacts")
class ArtifactSchema(BaseModel):
    artifact_id: str = ""
    message_id: str = ""
    conversation_id: str = ""
    artifact_type: str = ""
    record_created_time: str = ""
    path: str = ""
    
    @staticmethod
    def get_primary_key_name():
        return "artifact_id"


    