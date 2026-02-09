import json
import pickle
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from chatbot.nlp_engine import preprocess

MODEL_PATH = "models/intent_classifier.pkl"

def load_data():
    with open("data/intents.json") as f:
        data = json.load(f)
    return data["intents"]

def train():
    intents = load_data()

    texts = []
    labels = []

    for intent in intents:
        for pattern in intent["patterns"]:
            tokens = preprocess(pattern)
            texts.append(" ".join(tokens))
            labels.append(intent["tag"])

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression()
    model.fit(X, labels)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump((vectorizer, model), f)

    print("✅ Model trained and saved!")

def predict(text: str):
    with open(MODEL_PATH, "rb") as f:
        vectorizer, model = pickle.load(f)

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
