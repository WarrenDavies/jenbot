import os
import json
import yaml
from datetime import datetime
import textwrap

import requests
from audiorecorder.audio_recorder import AudioRecorder
from sttjenerator.models import registry

from jenbot.core.orchestrator import Orchestrator
 

with open("configs/core.yaml", 'r') as stream:
    core_config = yaml.safe_load(stream)

stt_config = {
    "model": "faster_whisper",
    "model_path": "medium",
    "audio": "inputs/example.wav"
}
stt_generator = registry.get_model_class(stt_config)
stt_generator.load()
stt_generator.warmup()

orchestrator = Orchestrator(core_config)

audio_recorder_config = {
    "sd_default_device": 7
}
audio_recorder = AudioRecorder(audio_recorder_config)

print("*** Chat — type 'exit' to quit. ***\n")
conversation_id = "ambient"
while True:


    if orchestrator.bot.mode == "ambient":
        user_input = input("You: ")
        conversation_id = orchestrator.process_ambient_mode()
        if conversation_id == "ambient":
            continue

    user_input = input("You: ")
    if user_input == "":
        np_audio = audio_recorder.record_until_enter_key_pressed()
        np_audio = np_audio.squeeze()
        stt_generator.config["audio"] = np_audio
        output = stt_generator.generate()
        user_input = " ".join([artifact.data for artifact in output.batch])
        print(user_input)
    if user_input.lower() in {"exit", "quit"}:
        break
    print()
    payload = {
        "conversation_id": conversation_id, 
        "content": user_input
    }

    response = orchestrator.process(payload)

    print(core_config["bot"]["name"] + ":", response)
    print("\n")