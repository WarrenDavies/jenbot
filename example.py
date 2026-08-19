import os
import config
import json

import requests


conversation_id = "test1234"

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
    "conversation_id": conversation_id,
    "number_of_messages": 10,
}
url = "http://127.0.0.1:8000/get_messages"
headers = {"Authorization": "Bearer YOUR_TOKEN", "Content-Type": "application/json"}
output = send_prompt(payload, url)

for message in output:
    print(message["role"] + ":", message["content"])
    print("\n\n\n")



while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        break

    payload = {
        "conversation_id": conversation_id, 
        "content": user_input
    }
    # call the API endpoint and generate output
    url = "http://127.0.0.1:8000/input"
    headers = {"Authorization": "Bearer YOUR_TOKEN", "Content-Type": "application/json"}
    output = send_prompt(payload, url)

    # Display response
    print("\n\n\n")
    print(config.bot["name"] + ":", output)
    print("\n\n\n")