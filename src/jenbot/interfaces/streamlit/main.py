import streamlit as st

st.title("Jenbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


with st.chat_message("user"):
    st.write("Hello 👋")

with st.chat_message("assistant"):
    st.write("Hello human")






if prompt := st.chat_input("Say something"):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    ## get bot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": prompt,
    })





# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])