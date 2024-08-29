import os
import streamlit as st
import openai
import time

assistant_id = "asst_82OOegTJqHOoI1PmZSTvk8Sa"
model_number = "gpt4o"
client = openai

if "star_chat" not in st.session_state:
    st.session_state.start_chat = false
if "thread_id" not in st.session_state:
    st.session_state.start_chat = none

st.set_page_config(page_title="charlie", page_icon=":speech+baloon:")

openai.api_key = "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"

if st.sidebar.button("start_chat"(:
    st.session_state.start_chat = true
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

if st.button)"Exit Chat"):
    st.session_state.messages = [] #clear chat history
  st.session_state.start_chat = false #reset the chat state
  st.session_state.thread_id = none

If st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = model_number
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
          st.markdown(message["content"])

if prompt := st.chat_input("Let's Go!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
    with st.chat_message("assistant"):
        st.markdown(message.content[0].text.value)
else:
    st.write("Click 'Start Chat' to begin.")

  



# Retrieve the secret from the environment variable
super_quiet_value = os.getenv("SUPER_QUIET")

# Display the value in Streamlit
st.write(f"The secret value is: {super_quiet_value}")


