"""
PyMate - Smart Chatbot (Streamlit Web Version)
Features: Casual chat + Live Weather + Shopping search links + GATE exam guidance
Run locally: streamlit run app.py
"""

import random
import re
from datetime import datetime
import requests
import streamlit as st

# ---------------- Basic Chit-Chat Responses ----------------
responses = {
    "hello": ["Hey there! 👋 Great to see you!", "Hello hello! What's on your mind today?"],
    "hi": ["Hiii! 😄 How's it going?", "Hey! Ready to chat?"],
    "how are you": ["I'm running at 100% CPU excitement! 🚀 How about you?"],
    "name": ["I'm PyMate — your friendly neighborhood chatbot! 🤖"],
    "time": [f"⏰ Right now it's {datetime.now().strftime('%H:%M:%S')}"],
    "date": [f"📅 Today's date is {datetime.now().strftime('%d-%m-%Y')}"],
    "bye": ["Catch you later! 👋", "Goodbye! Come back soon! ✨"],
    "help": [
        "Here's what I can do:\n"
        "- 💬 Just chat (say hello, ask my name, a joke...)\n"
        "- 🌦️ **Weather**: try 'weather in Delhi'\n"
        "- 🛒 **Shopping**: try 'buy wireless earphones'\n"
        "- 🎓 **GATE prep**: try 'gate cse suggestion'"
    ],
    "python": ["Python 🐍 is my home turf — great for AI, ML, and automation!"],
    "thank you": ["You're very welcome! 🙌"],
    "thanks": ["No problem at all! 😊"],
    "joke": [
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "Why did the developer go broke? Because they used up all their cache! 💸",
    ],
    "who made you": ["I was built by Bhanu Pratap Singh using pure Python logic! 💻"],
}

default_responses = [
    "Hmm 🤔 I'm not sure I follow — try rephrasing, or type 'help' to see what I can do!",
    "Interesting! Tell me more about that.",
]

quick_replies = ["👋 Hello", "🌦️ Weather in Noida", "🛒 Buy laptop", "🎓 Gate cse suggestion", "😂 Joke"]

GATE_RESOURCES = {
    "cse": {
        "subjects": "Data Structures, Algorithms, OS, DBMS, CN, Theory of Computation, Digital Logic",
        "tips": [
            "Start with core subjects: DS, Algorithms, and OS carry the most weightage.",
            "Practice previous 10 years' GATE papers subject-wise.",
            "Standard books: 'Introduction to Algorithms' (CLRS), Galvin (OS), Navathe (DBMS).",
            "Use GATE Overflow (gateoverflow.in) for solved previous-year questions.",
        ],
    },
    "ece": {
        "subjects": "Signals & Systems, Network Theory, Electronic Devices, Analog & Digital Circuits",
        "tips": [
            "Focus on Signals & Systems and Networks — highest weightage.",
            "Practice numerical-heavy previous year papers.",
            "Standard books: Sedra & Smith (Electronics), Oppenheim (Signals & Systems).",
        ],
    },
    "mechanical": {
        "subjects": "Thermodynamics, Fluid Mechanics, Strength of Materials, Manufacturing",
        "tips": [
            "Thermodynamics and SOM together carry major weightage.",
            "Practice formula-based numericals daily.",
            "Standard books: RS Khurmi, PK Nag (Thermodynamics).",
        ],
    },
}


def get_weather(city: str) -> str:
    """Fetch live weather using Open-Meteo (free, no API key needed)."""
    try:
        # Step 1: Get coordinates for the city
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geo_url, timeout=6).json()

        if not geo_res.get("results"):
            return f"Sorry, I couldn't find a place called '{city}' 🌍"

        place = geo_res["results"][0]
        lat, lon = place["latitude"], place["longitude"]
        place_name = place.get("name", city)

        # Step 2: Get current weather for those coordinates
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&current_weather=true"
        )
        weather_res = requests.get(weather_url, timeout=6).json()
        current = weather_res.get("current_weather", {})

        temp = current.get("temperature")
        wind = current.get("windspeed")

        if temp is None:
            return f"Couldn't fetch live weather for {place_name} right now. Try again later!"

        return (
            f"🌦️ **Weather in {place_name}**\n\n"
            f"🌡️ Temperature: {temp}°C\n"
            f"💨 Wind speed: {wind} km/h"
        )
    except Exception:
        return "⚠️ Couldn't reach the weather service right now. Please try again in a moment."


def get_shopping_links(query: str) -> str:
    """Generate direct search links for Amazon and Flipkart (no live scraping)."""
    search_term = query.strip().replace(" ", "+")
    amazon_link = f"https://www.amazon.in/s?k={search_term}"
    flipkart_link = f"https://www.flipkart.com/search?q={search_term}"
    return (
        f"🛒 I can't pull live product listings directly, but here are quick search links for **{query.strip()}**:\n\n"
        f"- 🅰️ [Search on Amazon]({amazon_link})\n"
        f"- 🅵 [Search on Flipkart]({flipkart_link})"
    )


def get_gate_suggestion(query: str) -> str:
    """Give GATE preparation suggestions based on branch mentioned."""
    branch = None
    if "cse" in query or "computer" in query:
        branch = "cse"
    elif "ece" in query or "electronics" in query:
        branch = "ece"
    elif "mech" in query:
        branch = "mechanical"

    if not branch:
        return (
            "🎓 Tell me your branch for GATE suggestions — try:\n"
            "'gate cse suggestion', 'gate ece suggestion', or 'gate mechanical suggestion'"
        )

    data = GATE_RESOURCES[branch]
    tips_text = "\n".join([f"- {tip}" for tip in data["tips"]])
    return (
        f"🎓 **GATE {branch.upper()} Preparation Guide**\n\n"
        f"**Key Subjects:** {data['subjects']}\n\n"
        f"**Tips:**\n{tips_text}"
    )


def get_response(user_input: str) -> str:
    text = user_input.lower().strip()

    # Intent: Weather
    if "weather" in text:
        match = re.search(r"weather (?:in|at|for)?\s*([a-zA-Z\s]+)", text)
        city = match.group(1).strip() if match and match.group(1).strip() else "Delhi"
        return get_weather(city)

    # Intent: Shopping
    if any(word in text for word in ["buy", "amazon", "flipkart", "shop", "purchase"]):
        product = re.sub(r"\b(buy|amazon|flipkart|shop|purchase|on|from|search|for|me|a|an)\b", "", text).strip()
        product = product if product else "product"
        return get_shopping_links(product)

    # Intent: GATE exam
    if "gate" in text:
        return get_gate_suggestion(text)

    # Fallback: keyword-based chit-chat
    if text in ["exit", "quit", "bye"]:
        return random.choice(responses["bye"])

    for keyword, reply_list in responses.items():
        if keyword in text:
            return random.choice(reply_list)

    return random.choice(default_responses)


# ---------------- Page Config ----------------
st.set_page_config(page_title="PyMate 🤖", page_icon="🤖", layout="centered")

# ---------------- Custom CSS ----------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
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

# ---------------- Chat State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hey! I'm **PyMate** 🤖 — I can chat, check live weather, find shopping links, "
            "and guide you on GATE prep. Type 'help' or tap a quick reply below!",
        }
    ]

# ---------------- Quick Reply Buttons ----------------
cols = st.columns(len(quick_replies))
quick_click = None
for col, qr in zip(cols, quick_replies):
    if col.button(qr, use_container_width=True):
        quick_click = qr.split(" ", 1)[1]

st.divider()

# ---------------- Display Chat History ----------------
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else "🧑"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------------- Handle Input ----------------
user_input = st.chat_input("Type your message here...")
final_input = user_input or quick_click

if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(final_input)

    with st.spinner("PyMate is thinking..."):
        bot_reply = get_response(final_input)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_reply)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("### ⚙️ About PyMate")
    st.write("Built with **Python** + **Streamlit**.")
    st.write("Features: Chat, Live Weather (Open-Meteo API), Shopping search links, GATE guidance.")
    st.write("Built by **Bhanu Pratap Singh**")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared! Let's start fresh 🌱"}
        ]
        st.rerun()
