from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import uuid
import datetime

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):

    model_config = ConfigDict(extra='allow')

    @property
    def extra_data(self) -> Dict[str, Any]:
        return self.model_extra or {}


    @classmethod
    def get_primary_key_name(cls) -> str:
        # returns first field by default
        return next(iter(cls.__fields__.keys()))
        