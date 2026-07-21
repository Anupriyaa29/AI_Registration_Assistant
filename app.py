from flask import Flask, render_template, request, jsonify
import json
import random
import joblib

from utils.preprocess import preprocess

app = Flask(__name__)

# Load model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Load intents
with open("data/intents.json", "r") as file:
    intents = json.load(file)


def get_response(tag):
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "Sorry, I don't understand."


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    processed = preprocess(user_message)
    processed = " ".join(processed)

    vector = vectorizer.transform([processed])

    prediction = model.predict(vector)[0]

    response = get_response(prediction)

    return jsonify({"response": response})