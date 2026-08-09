"""
Simple Rule-Based Chatbot - Streamlit Web Version
Run locally: streamlit run app.py
Deploy on Render, Streamlit Cloud, or any Python host.
"""

import random
from datetime import datetime
import streamlit as st

# Keyword -> Possible Responses
responses = {
    "hello": ["Hi there! How can I help you today?", "Hello! What's up?"],
    "hi": ["Hey! How are you doing?", "Hi! Nice to see you."],
    "how are you": ["I'm just a bot, but I'm doing great! How about you?"],
    "name": ["I'm a simple chatbot built in Python!", "You can call me PyBot."],
    "time": [f"The current time is {datetime.now().strftime('%H:%M:%S')}"],
    "date": [f"Today's date is {datetime.now().strftime('%d-%m-%Y')}"],
    "bye": ["Goodbye! Have a great day!", "See you later!"],
    "help": ["You can ask me about: hello, name, time, date, weather, or just chat!"],
    "weather": ["I can't check live weather yet, but you can ask a weather API for that!"],
    "python": ["Python is a great language for AI/ML and automation!"],
    "thank you": ["You're welcome!", "No problem at all!"],
    "thanks": ["Anytime!", "Glad I could help!"],
}

default_responses = [
    "I'm not sure I understand. Can you rephrase that?",
    "Interesting! Tell me more.",
    "Hmm, I don't have an answer for that yet.",
    "Can you ask that in a different way?",
]


def get_response(user_input: str) -> str:
    user_input = user_input.lower().strip()
    for keyword, reply_list in responses.items():
        if keyword in user_input:
            return random.choice(reply_list)
    return random.choice(default_responses)


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="PyBot - Simple Chatbot", page_icon="🤖")

st.title("🤖 PyBot - Simple Chatbot")
st.caption("A rule-based chatbot built with Python & Streamlit")

# Chat history stored in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm PyBot. Ask me something (try 'hello', 'time', 'help')."}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    bot_reply = get_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.write(bot_reply)
