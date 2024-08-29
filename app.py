import os
import streamlit as st
import openai
import time

# Use the API key from Streamlit secrets
try:
    openai_api_key = st.secrets["api_keys"]["openai"]
    openai.api_key = openai_api_key
except KeyError:
    st.error("OpenAI API key is missing in the secrets.")
    st.stop()

assistant_id = "asst_82OOegTJqHOoI1PmZSTvk8Sa"
model_number = "gpt4o"
client = openai

try:
    if "start_chat" not in st.session_state:
        st.session_state.start_chat = False
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None

    st.set_page_config(page_title="charlie", page_icon=":speech_balloon:")

    if st.sidebar.button("start_chat"):
        st.session_state.start_chat = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    if st.button("Exit Chat"):
        st.session_state.messages = []  # clear chat history
        st.session_state.start_chat = False  # reset the chat state
        st.session_state.thread_id = None

    if st.session_state.start_chat:
        if "openai_model" not in st.session_state:
            st.session_state.openai_model = model_number
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            st.write(f"{message['role']}: {message['content']}")  # Simplified for demonstration

    if prompt := st.chat_input("Let's Go!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.write(f"user: {prompt}")

        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions="Please answer the queries with meows as you are a cat."
        )
        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )

        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages
            if message.run_id == run.id and message.role == "assistant"
        ]

        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content})
            st.write(f"assistant: {message.content}")

except Exception as e:
    st.error(f"An error occurred: {e}")
    st.stop()

# Retrieve the secret from the environment variable
super_quiet_value = os.getenv("SUPER_QUIET")

# Display the value in Streamlit
if super_quiet_value:
    st.write(f"The secret value is: {super_quiet_value}")
else:
    st.error("The SUPER_QUIET environment variable is missing.")
