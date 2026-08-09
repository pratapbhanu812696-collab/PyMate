"""
PyMate - CLI Version (with color!)
Run this in VS Code terminal: python chatbot_cli.py
"""

import random
import time
from datetime import datetime

# ANSI color codes for a more fun terminal look
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

responses = {
    "hello": ["Hey there! 👋 Great to see you!", "Hello hello! What's on your mind today?"],
    "hi": ["Hiii! 😄 How's it going?", "Hey! Ready to chat?"],
    "how are you": ["I'm running at 100% CPU excitement! 🚀 How about you?", "Feeling electric today! ⚡ You?"],
    "name": ["I'm PyMate — your friendly neighborhood chatbot! 🤖", "Call me PyMate. I live in Python and love good conversations!"],
    "time": [f"⏰ Right now it's {datetime.now().strftime('%H:%M:%S')}"],
    "date": [f"📅 Today's date is {datetime.now().strftime('%d-%m-%Y')}"],
    "bye": ["Catch you later! 👋", "Goodbye! Come back soon! ✨"],
    "help": ["Try asking me: hello, my name, the time, the date, a joke, or about Python! 🎯"],
    "weather": ["I can't check live weather yet ☁️, but I'm sunny inside!"],
    "python": ["Python 🐍 is my home turf — great for AI, ML, and automation!"],
    "thank you": ["You're very welcome! 🙌", "Anytime, that's what I'm here for!"],
    "thanks": ["No problem at all! 😊", "Glad I could help!"],
    "joke": [
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "Why did the developer go broke? Because they used up all their cache! 💸",
    ],
    "who made you": ["I was built by Bhanu Pratap Singh using pure Python logic! 💻"],
}

default_responses = [
    "Hmm 🤔 I'm not sure I follow — try rephrasing?",
    "Interesting! Tell me more about that.",
    "I don't have an answer for that yet, but I'm learning! 🌱",
    "Can you ask that a little differently?",
]


def get_response(user_input: str) -> str:
    user_input = user_input.lower().strip()
    if user_input in ["exit", "quit", "bye"]:
        return random.choice(responses["bye"])
    for keyword, reply_list in responses.items():
        if keyword in user_input:
            return random.choice(reply_list)
    return random.choice(default_responses)


def type_effect(text: str, delay: float = 0.015):
    """Bot ka reply thoda 'typing' effect ke saath print hota hai."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def main():
    print(f"{MAGENTA}{BOLD}{'=' * 55}{RESET}")
    print(f"{CYAN}{BOLD}          🤖  P y M a t e   C h a t b o t  🤖{RESET}")
    print(f"{MAGENTA}{BOLD}{'=' * 55}{RESET}")
    print(f"{YELLOW}Type 'help' to see what I can do, or 'exit' to quit.{RESET}\n")

    while True:
        user_input = input(f"{GREEN}{BOLD}You: {RESET}")

        if user_input.lower().strip() in ["exit", "quit"]:
            print(f"{CYAN}{BOLD}PyMate: {RESET}", end="")
            type_effect(random.choice(responses["bye"]))
            break

        bot_reply = get_response(user_input)
        print(f"{CYAN}{BOLD}PyMate: {RESET}", end="")
        type_effect(bot_reply)


if __name__ == "__main__":
    main()
