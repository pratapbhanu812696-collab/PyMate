"""
Simple Rule-Based Chatbot - CLI Version
Run this in VS Code terminal: python chatbot_cli.py
"""

import random
from datetime import datetime

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
    if user_input in ["exit", "quit", "bye"]:
        return random.choice(responses["bye"])
    for keyword, reply_list in responses.items():
        if keyword in user_input:
            return random.choice(reply_list)
    return random.choice(default_responses)


def main():
    print("=" * 50)
    print("  Simple Python Chatbot (type 'exit' to quit)")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ")
        if user_input.lower().strip() in ["exit", "quit"]:
            print("Bot:", random.choice(responses["bye"]))
            break
        print("Bot:", get_response(user_input))


if __name__ == "__main__":
    main()
