import json
import random
import joblib

from utils.preprocess import preprocess

# Load trained model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Load intents
with open("data/intents.json", "r") as file:
    data = json.load(file)
    
def get_response(tag):
    for intent in data["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
        
while True:

    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Bot: Goodbye!")
        break

    processed = preprocess(user_input)
    processed = " ".join(processed)

    vector = vectorizer.transform([processed])

    probabilities = model.predict_proba(vector)
    confidence = max(probabilities[0])
    prediction = model.predict(vector)[0]

    if confidence < 0.40:
        print("Bot: I'm sorry, I can currently help only with registration-related questions.")
    else:
        response = get_response(prediction)
        print("Bot:", response)