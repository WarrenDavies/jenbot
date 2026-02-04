import os
import json
import yaml
from datetime import datetime
import textwrap

import requests

from jenbot.core.orchestrator import Orchestrator
 

with open("configs/core.yaml", 'r') as stream:
    core_config = yaml.safe_load(stream)

orchestrator = Orchestrator(core_config)

print("*** Chat — type 'exit' to quit. ***\n")
while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        break
    print()
    payload = {
        "conversation_id": "mem_test3", 
        "content": user_input
    }

    response = orchestrator.process(payload)

    print(core_config["bot"]["name"] + ":", response)
    print("\n")