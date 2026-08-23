import yaml
import uuid
import datetime

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
    st.session_state.active_conversation_id = str(uuid.uuid4())

if "requested_conversation_id" not in st.session_state:
    st.session_state.requested_conversation_id = st.session_state.active_conversation_id



number_of_messages = 100


### set up

@st.cache_resource
def load_orchestrator(core_config):
    return Orchestrator(core_config)
orchestrator = load_orchestrator(core_config)

if "conversations" not in st.session_state:
    st.session_state.conversations = (
        orchestrator.bot.memory_manager.get_conversation_ids()
    )

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






### render

st.title("Jenbot")


with st.sidebar:

    st.markdown("## Jenbot")

    if st.sidebar.button("New Chat", key=f"New Chat", use_container_width=True):
        st.session_state.requested_conversation_id = str(uuid.uuid4())
        st.rerun()

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
        "conversation_id": st.session_state.active_conversation_id, 
        "content": prompt,
        "source": "web",
    }
    response = orchestrator.process(payload)
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
    })

    with st.chat_message("assistant"):
        st.markdown(response)

    if st.session_state.active_conversation_id not in (
        [conversation["conversation_id"] for conversation in st.session_state.conversations]
    ):
        st.session_state.conversations.insert(
            0,
            {
                "conversation_id": st.session_state.active_conversation_id,
                "latest_message_ts": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                "message_count": 2,
            }
        )   
    else: 
        for conversation in st.session_state.conversations:
            if conversation["conversation_id"] == st.session_state.active_conversation_id:
                conversation["message_count"] += 2
                conversation["latest_message_ts"] = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                break

        if st.session_state.active_conversation_id != st.session_state.conversations[0]["conversation_id"]:
            st.session_state.conversations = sorted(
                st.session_state.conversations, 
                key=lambda x: x['latest_message_ts'],
                reverse=True,
            )
    

