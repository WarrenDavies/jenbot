from typing import Union
from datetime import datetime
import yaml
import json
import textwrap

from fastapi import FastAPI

from jenbot.core.orchestrator import Orchestrator


with open("configs/core.yaml", 'r') as stream:
    core_config = yaml.safe_load(stream)

app = FastAPI()
orchestrator = Orchestrator(core_config)

@app.post("/input")
def read_item(payload: dict):
    payload["source"] = "api"
    message = payload["content"]
    current_time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = orchestrator.process(payload)
    response = f"""
    The time is: {current_time_string}
    Your input was: {message}
    Response: {json.dumps(response)}
    """
    response = textwrap.dedent(response)
    return response


@app.post("/get_messages")
def read_item(message: dict):

    conversation_id = message["conversation_id"]
    number_of_messages = message.get("number_of_messages")
    
    response = orchestrator.bot.memory_manager.get_recent_messages(
        conversation_id,
        number_of_messages
    )
    return response