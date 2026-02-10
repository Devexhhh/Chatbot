import json
import pickle
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from chatbot.nlp_engine import preprocess

MODEL_PATH = "models/intent_classifier.pkl"

# 🔥 Load once at startup
with open(MODEL_PATH, "rb") as f:
    vectorizer, model = pickle.load(f)

def load_data():
    with open("data/intents.json") as f:
        data = json.load(f)
    return data["intents"]

def predict(text: str):
    tokens = preprocess(text)
    X = vectorizer.transform([" ".join(tokens)])

    probs = model.predict_proba(X)[0]
    max_prob = max(probs)
    intent = model.classes_[probs.argmax()]

    return intent, max_prob

def get_response(intent: str):
    intents = load_data()
    for i in intents:
        if i["tag"] == intent:
            return random.choice(i["responses"])

    return "I didn't understand that 🤔"
