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
def read_item(message: dict):
    last_message = message["messages"][-1]["content"]
    current_time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = orchestrator.process(message)
    response = f"""
    The time is: {current_time_string}
    Your input was: {last_message}
    Response: {json.dumps(response)}
    """
    response = textwrap.dedent(response)
    return response