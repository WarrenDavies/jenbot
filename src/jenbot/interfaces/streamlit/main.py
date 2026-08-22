import yaml
import uuid

import streamlit as st

from audiorecorder.audio_recorder import AudioRecorder
from sttjenerator.models import registry

from jenbot.core.orchestrator import Orchestrator


### config
with open("configs/core.yaml", 'r') as stream:
    core_config = yaml.safe_load(stream)

with open("configs/interface.yaml", 'r') as stream:
    interface_config = yaml.safe_load(stream)

if "active_conversation_id" not in st.session_state:
    st.session_state.active_conversation_id = "test1234"

if "requested_conversation_id" not in st.session_state:
    st.session_state.requested_conversation_id = "test1234"

number_of_messages = 100


### set up

@st.cache_resource
def load_orchestrator(core_config):
    return Orchestrator(core_config)
orchestrator = load_orchestrator(core_config)


conversation_changed = (
    st.session_state.requested_conversation_id != st.session_state.active_conversation_id
)

if ("messages" not in st.session_state) or conversation_changed:

    st.session_state.active_conversation_id = st.session_state.requested_conversation_id

    messages = orchestrator.bot.memory_manager.get_recent_messages(
        st.session_state.active_conversation_id,
        number_of_messages
    )
    if not messages:
        messages = []
    st.session_state.messages = messages



if "conversations" not in st.session_state:
    st.session_state.conversations = (
        orchestrator.bot.memory_manager.get_conversation_ids()
    )



### render

st.title("Jenbot")


with st.sidebar:

    st.markdown("### 💬 Chats")

    conversation_text = st.empty()
    for conversation in st.session_state.conversations:
        conversation_id = conversation["conversation_id"]
        count = conversation["message_count"]
        is_active = st.session_state.active_conversation_id == conversation_id

        label = f"{'▶ ' if is_active else ''}{conversation_id} ({count})"

        if st.sidebar.button(label, key=f"btn_{conversation_id}", use_container_width=True):
            st.session_state.requested_conversation_id = conversation_id
            st.rerun()




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
        "content": prompt,
        "source": "api",
    }
    response = orchestrator.process(payload)
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
    })

    with st.chat_message("assistant"):
        st.markdown(response)

