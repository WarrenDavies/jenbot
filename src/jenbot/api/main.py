from typing import Union
from datetime import datetime

from fastapi import FastAPI

app = FastAPI()

@app.post("/input")
def read_item(prompt: dict):
    last_message = prompt["messages"][-1]["content"]
    current_time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""
The time is: {current_time_string}
Your input was: {last_message}"""