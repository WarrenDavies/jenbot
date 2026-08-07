import os
import config
import json

import requests


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


payload = {
    "conversation_id": "test1234",
    "number_of_messages": 10,
}
url = "http://127.0.0.1:8000/get_messages"
headers = {"Authorization": "Bearer YOUR_TOKEN", "Content-Type": "application/json"}
output = send_prompt(payload, url)

for message in output:
    print(message)




while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        break

    # keep track of user input
    current_message = {"role": "user", "content": user_input}
    messages.append(current_message)

    payload = {"messages": messages}
    # call the API endpoint and generate output
    url = "http://127.0.0.1:8000/input"
    headers = {"Authorization": "Bearer YOUR_TOKEN", "Content-Type": "application/json"}
    output = send_prompt(payload, url)

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