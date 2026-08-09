"""
intent_classifier.py
Lightweight ML-based intent detection using TF-IDF + Cosine Similarity.
This replaces naive keyword matching with a proper NLP approach —
the bot can now recognize similar/paraphrased sentences, not just exact keywords.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Training examples: several ways a user might phrase each intent.
# More examples per intent = better generalization.
INTENT_EXAMPLES = {
    "greeting": ["hello", "hi", "hey", "hey there", "good morning", "good evening", "yo", "what's up"],
    "how_are_you": ["how are you", "how are you doing", "how's it going", "how do you feel"],
    "name": ["what is your name", "who are you", "what should I call you", "your name please"],
    "time": ["what time is it", "tell me the time", "current time", "what's the time now"],
    "date": ["what is the date today", "tell me today's date", "what's today's date"],
    "bye": ["bye", "goodbye", "see you later", "exit", "quit", "talk to you later"],
    "help": ["help", "what can you do", "show me your features", "what do you do", "how can you help me"],
    "python": ["tell me about python", "what is python", "python language"],
    "thanks": ["thank you", "thanks", "thank you so much", "appreciate it"],
    "joke": ["tell me a joke", "make me laugh", "say something funny", "know any jokes"],
    "who_made_you": ["who made you", "who built you", "who created you", "who developed you"],
    "weather": [
        "what is the weather", "weather in delhi", "tell me the weather",
        "how's the weather today", "weather forecast", "is it raining",
        "weather at noida", "weather for mumbai",
    ],
    "shopping": [
        "buy a laptop", "i want to buy shoes", "shop for a phone",
        "purchase headphones", "search amazon for a bag", "find this on flipkart",
        "buy wireless earphones",
    ],
    "gate": [
        "gate exam preparation", "gate cse suggestion", "how to prepare for gate",
        "gate exam tips", "gate syllabus", "gate ece guidance",
    ],
}

# Minimum similarity score to trust a match; below this we fall back to "unknown"
CONFIDENCE_THRESHOLD = 0.35


class IntentClassifier:
    def __init__(self):
        self.intents = []
        self.examples = []
        for intent, phrases in INTENT_EXAMPLES.items():
            for phrase in phrases:
                self.intents.append(intent)
                self.examples.append(phrase)

        # Fit TF-IDF vectorizer on all training examples
        self.vectorizer = TfidfVectorizer()
        self.example_vectors = self.vectorizer.fit_transform(self.examples)

    def classify(self, text: str):
        """
        Returns (intent, confidence_score).
        If confidence is below threshold, returns ("unknown", score).
        """
        text = text.lower().strip()
        if not text:
            return "unknown", 0.0

        input_vector = self.vectorizer.transform([text])
        similarities = cosine_similarity(input_vector, self.example_vectors)[0]

        best_idx = similarities.argmax()
        best_score = similarities[best_idx]
        best_intent = self.intents[best_idx]

        if best_score < CONFIDENCE_THRESHOLD:
            return "unknown", float(best_score)

        return best_intent, float(best_score)


# Singleton instance — built once, reused across requests
classifier = IntentClassifier()


def detect_intent(text: str):
    """Convenience wrapper used by app.py"""
    return classifier.classify(text)
