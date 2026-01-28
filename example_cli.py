import os
import config
import json
import yaml
from datetime import datetime
import textwrap

import requests

from jenbot.core.orchestrator import Orchestrator
 

with open("configs/core.yaml", 'r') as stream:
    core_config = yaml.safe_load(stream)

orchestrator = Orchestrator(core_config)


messages = [config.bot["system_prompt"]]
messages_all = [config.bot["system_prompt"]]
print("*** Chat — type 'exit' to quit. ***\n")

def send_prompt(payload, url):
    resp = requests.post(
        url, 
        json=payload, 
        headers=headers, 
        timeout=10
    )
    resp.raise_for_status()
    data = resp.json()
    return data


while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        break

    payload = {"content": user_input}

    response = orchestrator.process(payload)

    print(config.bot["name"] + ":", response)
    print("\n")