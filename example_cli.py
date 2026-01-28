import os
import config
import json
import yaml
from datetime import datetime
import textwrap

import requests

from src.jenbot.core.orchestrator import Orchestrator
 

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

    # keep track of user input
    current_message = {"role": "user", "content": user_input}
    messages.append(current_message)

    payload = {"messages": messages}
    print(messages)
    last_message = payload["messages"][-1]["content"]
    current_time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = orchestrator.process(payload)
    response = f"""
    The time is: {current_time_string}
    Your input was: {last_message}
    Response: {json.dumps(response)}
    """
    output = textwrap.dedent(response)

    # keep track of bot responses
    messages.append({"role": "assistant", "content": output})

    # to keep responses faster, limit the number of messages we put in the context
    if len(messages) > config.messages_to_keep_in_context:
        if config.messages_to_keep_in_context == 0:
            messages = [config.bot["system_prompt"]]
        else:
            messages = [config.bot["system_prompt"]] + messages[-config.messages_to_keep_in_context:]

    # Display response
    print("\n")
    print(config.bot["name"] + ":", output)
    print("\n")