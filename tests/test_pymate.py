"""
tests/test_pymate.py
Unit tests for PyMate's core logic: intent classification, weather parsing,
shopping link generation, GATE suggestions, and database operations.

Run with: pytest tests/ -v
"""

import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from intent_classifier import detect_intent
from handlers import get_shopping_links, get_gate_suggestion, GATE_RESOURCES
import database


# ---------------- Intent Classifier Tests ----------------
class TestIntentClassifier:
    def test_greeting_intent(self):
        intent, confidence = detect_intent("hello there")
        assert intent == "greeting"
        assert confidence > 0.3

    def test_weather_intent(self):
        intent, confidence = detect_intent("what's the weather in mumbai")
        assert intent == "weather"

    def test_shopping_intent(self):
        intent, confidence = detect_intent("i want to buy a laptop")
        assert intent == "shopping"

    def test_gate_intent(self):
        intent, confidence = detect_intent("how do I prepare for gate exam")
        assert intent == "gate"

    def test_joke_intent(self):
        intent, confidence = detect_intent("tell me a joke")
        assert intent == "joke"

    def test_unknown_intent_for_gibberish(self):
        intent, confidence = detect_intent("asdkfj qpwoeiru xyz123")
        assert intent == "unknown"

    def test_empty_input(self):
        intent, confidence = detect_intent("")
        assert intent == "unknown"
        assert confidence == 0.0

    def test_paraphrased_greeting(self):
        # Tests that ML approach generalizes beyond exact keyword match
        intent, confidence = detect_intent("hey there, good morning")
        assert intent == "greeting"


# ---------------- Shopping Link Tests ----------------
class TestShoppingLinks:
    def test_generates_both_links(self):
        result = get_shopping_links("laptop")
        assert "amazon.in" in result
        assert "flipkart.com" in result

    def test_handles_multi_word_product(self):
        result = get_shopping_links("wireless earphones")
        assert "wireless+earphones" in result

    def test_link_format_is_valid_markdown(self):
        result = get_shopping_links("phone")
        assert "[Search on Amazon]" in result
        assert "[Search on Flipkart]" in result


# ---------------- GATE Suggestion Tests ----------------
class TestGateSuggestion:
    def test_cse_branch_detected(self):
        result = get_gate_suggestion("gate cse suggestion")
        assert "CSE" in result
        assert "Data Structures" in result

    def test_ece_branch_detected(self):
        result = get_gate_suggestion("gate ece guidance")
        assert "ECE" in result

    def test_mechanical_branch_detected(self):
        result = get_gate_suggestion("gate mechanical tips")
        assert "MECHANICAL" in result

    def test_no_branch_asks_for_clarification(self):
        result = get_gate_suggestion("gate exam")
        assert "Tell me your branch" in result

    def test_all_branches_have_required_fields(self):
        for branch, data in GATE_RESOURCES.items():
            assert "subjects" in data
            assert "tips" in data
            assert len(data["tips"]) > 0


# ---------------- Database Tests ----------------
class TestDatabase:
    TEST_SESSION = "test-session-001"

    def setup_method(self):
        database.init_db()

    def test_save_and_retrieve_message(self):
        database.save_message(self.TEST_SESSION, "user", "hello test")
        history = database.get_history(self.TEST_SESSION, limit=5)
        assert len(history) > 0
        assert any("hello test" in row[1] for row in history)

    def test_save_message_with_intent(self):
        database.save_message(self.TEST_SESSION, "assistant", "Hi!", intent="greeting")
        history = database.get_history(self.TEST_SESSION, limit=5)
        assert len(history) > 0
