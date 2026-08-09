"""
PyMate - Smart Chatbot (Streamlit Web Version)
This file handles ONLY the UI layer. All business logic lives in handlers.py,
intent_classifier.py, and database.py — keeping concerns separated and testable.

Run locally: streamlit run app.py
"""

import logging
import uuid

import streamlit as st

from handlers import get_response
from database import init_db, save_message, get_history

# ---------------- Logging Setup ----------------
logging.basicConfig(
    filename="pymate.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# ---------------- Database Init ----------------
init_db()

# ---------------- Page Config ----------------
st.set_page_config(page_title="PyMate 🤖", page_icon="🤖", layout="centered")

# ---------------- Custom CSS ----------------
st.markdown(
    """
    <style>
    .stApp {
        background: #000000;
    }
    .main-header {
        text-align: center;
        padding: 1.2rem 0 0.3rem 0;
    }
    .main-header h1 {
        font-size: 2.4rem;
        background: linear-gradient(90deg, #00f5a0, #00d9f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0;
    }
    .main-header p {
        color: #c9c9e0;
        font-size: 0.95rem;
        margin-top: 0.2rem;
    }
    div[data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 4px 6px;
    }
    .stChatInput textarea {
        border-radius: 20px !important;
    }
    div.stButton > button {
        border-radius: 20px;
        border: 1px solid #00d9f5;
        background: rgba(0, 217, 245, 0.08);
        color: #e6e6fa;
        padding: 4px 14px;
        font-size: 0.85rem;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #00f5a0, #00d9f5);
        color: #0f0c29;
        border: 1px solid transparent;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Header ----------------
st.markdown(
    """
    <div class="main-header">
        <h1>🤖 PyMate</h1>
        <p>Chat • Weather • Shopping Links • GATE Prep — all in one bot</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- Session ID (for chat history persistence) ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ---------------- Chat State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hey! I'm **PyMate** 🤖 — I can chat, check live weather, find shopping links, "
            "and guide you on GATE prep. Type 'help' to see everything I can do!",
        }
    ]

# ---------------- Display Chat History ----------------
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else "🧑"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------------- Handle Input ----------------
final_input = st.chat_input("Type your message here...")

if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(final_input)
    save_message(st.session_state.session_id, "user", final_input)

    with st.spinner("PyMate is thinking..."):
        bot_reply, detected_intent = get_response(final_input)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_reply)
    save_message(st.session_state.session_id, "assistant", bot_reply, intent=detected_intent)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("### ⚙️ About PyMate")
    st.write("Built with **Python** + **Streamlit** + **scikit-learn**.")
    st.write(
        "Features: ML-based intent detection, Live Weather (Open-Meteo API), "
        "Shopping search links, GATE guidance, Chat history (SQLite), Logging."
    )
    st.write("Built by **Bhanu Pratap Singh**")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared! Let's start fresh 🌱"}
        ]
        st.rerun()

    with st.expander("🕘 View Past History (this session)"):
        history = get_history(st.session_state.session_id, limit=20)
        if not history:
            st.write("No history yet.")
        else:
            for role, content, ts in history:
                st.caption(f"{ts[:19]} — **{role}**: {content[:60]}")
