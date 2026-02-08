# chatbot/rule_based.py

import random
from chatbot.responses import RESPONSES
from chatbot.nlp_engine import preprocess

INTENTS = {
    "greeting": ["hi", "hello", "hey"],
    "goodbye": ["bye", "goodbye"],
    "thanks": ["thank", "thanks"],
    "help": ["help", "assist", "support"]
}

def detect_intent(user_input: str) -> str:
    tokens = preprocess(user_input)

    for intent, keywords in INTENTS.items():
        for token in tokens:
            if token in keywords:
                return intent

    return "unknown"

def get_response(intent: str) -> str:
    return random.choice(RESPONSES[intent])

def chatbot_reply(user_input: str) -> str:
    intent = detect_intent(user_input)
    return get_response(intent)
