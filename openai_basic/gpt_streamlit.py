import streamlit as st
import random
import time
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


st.write("Streamlit loves LLMs! 🤖 [Build your own chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) in minutes, then make it powerful by adding images, dataframes, or even input widgets to the chat.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "system":
        continue  # system 메시지는 UI에 표시 안함

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("메세지를 입력하세요..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            assistant_response = client.responses.create(
                model="gpt-4o-mini",
                temperature=0.3,
                input=st.session_state.messages
            )

            ai_text = assistant_response.output_text
            
        
        # Simulate stream of response with milliseconds delay
            for chunk in ai_text.split():
                full_response += chunk + " "
                time.sleep(0.05)
            # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"에러 발생: {str(e)}"
            message_placeholder.markdown(full_response)

    # AI 메시지 저장
    st.session_state.messages.append({"role": "assistant", "content": full_response})
