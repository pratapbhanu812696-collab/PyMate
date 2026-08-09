"""
handlers.py
Core business logic for PyMate — separated from the Streamlit UI layer.
This separation (UI vs logic) makes the code testable without needing
Streamlit installed, and follows good software engineering practice.
"""

import logging
import random
import re
from datetime import datetime

import requests

from intent_classifier import detect_intent

logger = logging.getLogger("pymate")

# ---------------- Static Response Banks ----------------
responses = {
    "greeting": ["Hey there! 👋 Great to see you!", "Hello hello! What's on your mind today?"],
    "how_are_you": ["I'm running at 100% CPU excitement! 🚀 How about you?"],
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
    "thanks": ["You're very welcome! 🙌", "No problem at all! 😊"],
    "joke": [
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "Why did the developer go broke? Because they used up all their cache! 💸",
    ],
    "who_made_you": ["I was built by Bhanu Pratap Singh using pure Python logic! 💻"],
}

default_responses = [
    "Hmm 🤔 I'm not sure I follow — try rephrasing, or type 'help' to see what I can do!",
    "Interesting! Tell me more about that.",
]

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


# ---------------- Feature Handlers ----------------
def get_weather(city: str) -> str:
    """Fetch live weather using Open-Meteo (free, no API key needed)."""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geo_url, timeout=6).json()

        if not geo_res.get("results"):
            return f"Sorry, I couldn't find a place called '{city}' 🌍"

        place = geo_res["results"][0]
        lat, lon = place["latitude"], place["longitude"]
        place_name = place.get("name", city)

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
    except Exception as e:
        logger.error(f"Weather API failed for city='{city}': {e}")
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


def get_response(user_input: str):
    """
    Main routing function.
    Uses the ML intent classifier to determine what the user wants,
    then dispatches to the right handler.
    Returns (reply_text, detected_intent) — intent is logged/saved for analytics.
    """
    text = user_input.lower().strip()
    intent, confidence = detect_intent(text)
    logger.info(f"Input='{user_input}' | Intent='{intent}' | Confidence={confidence:.2f}")

    try:
        if intent == "weather":
            match = re.search(r"weather (?:in|at|for)?\s*([a-zA-Z\s]+)", text)
            city = match.group(1).strip() if match and match.group(1).strip() else "Delhi"
            return get_weather(city), intent

        if intent == "shopping":
            product = re.sub(
                r"\b(buy|amazon|flipkart|shop|purchase|on|from|search|for|me|a|an|i|want|to)\b", "", text
            ).strip()
            product = product if product else "product"
            return get_shopping_links(product), intent

        if intent == "gate":
            return get_gate_suggestion(text), intent

        if intent in responses:
            return random.choice(responses[intent]), intent

        return random.choice(default_responses), "unknown"

    except Exception as e:
        logger.error(f"Error handling input='{user_input}': {e}")
        return "⚠️ Something went wrong on my end. Please try again!", "error"
