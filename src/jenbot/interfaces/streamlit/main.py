import yaml

import streamlit as st

from audiorecorder.audio_recorder import AudioRecorder
from sttjenerator.models import registry

from jenbot.core.orchestrator import Orchestrator


### config
with open("configs/core.yaml", 'r') as stream:
    core_config = yaml.safe_load(stream)

st.session_state.conversation_id = "test1234"
number_of_messages = 10

with open("configs/interface.yaml", 'r') as stream:
    interface_config = yaml.safe_load(stream)


### set up

@st.cache_resource
def load_orchestrator(core_config):
    return Orchestrator(core_config)
orchestrator = load_orchestrator(core_config)



if "messages" not in st.session_state:
    messages = orchestrator.bot.memory_manager.get_recent_messages(
        st.session_state.conversation_id,
        number_of_messages
    )
    if not messages:
        messages = []
    st.session_state.messages = messages



### render

st.title("Jenbot")
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



if prompt := st.chat_input("Say something"):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    ### process input
    payload = {
        "conversation_id": st.session_state.conversation_id, 
        "content": prompt
    }
    response = orchestrator.process(payload)
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
    })

    with st.chat_message("assistant"):
        st.markdown(response)

