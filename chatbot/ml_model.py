import json
import pickle
import random
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from chatbot.nlp_engine import preprocess

MODEL_PATH = Path("models/intent_classifier.pkl")
DATA_PATH = Path("data/intents.json")

vectorizer = None
model = None


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["intents"]


def train():
    intents = load_data()

    texts = []
    labels = []

    for intent in intents:
        for pattern in intent["patterns"]:
            tokens = preprocess(pattern)
            texts.append(" ".join(tokens))
            labels.append(intent["tag"])

    vec = TfidfVectorizer()
    X = vec.fit_transform(texts)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, labels)

    MODEL_PATH.parent.mkdir(exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump((vec, clf), f)

    print("Model trained and saved.")


def load_model():
    global vectorizer, model

    if vectorizer is None or model is None:
        with open(MODEL_PATH, "rb") as f:
            vectorizer, model = pickle.load(f)


def predict(text: str):
    load_model()

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

    return "I didn't understand that."
