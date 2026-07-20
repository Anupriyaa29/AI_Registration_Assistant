import json
import random
import joblib
import re

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

def register_user():
    user = {}

    print("\n----- Registration Form -----")

    user["name"] = input("Enter your full name: ")

    while True:
        email = input("Enter your email: ")

        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            user["email"] = email
            break

        print("Invalid email. Please try again.")

    while True:
        phone = input("Enter your phone number: ")
        if phone.isdigit() and len(phone) == 10:
            user["phone"] = phone
            break
        print("Phone number must contain exactly 10 digits.")
    user["college"] = input("Enter your college name: ")
    user["branch"] = input("Enter your branch: ")
    while True:
        year = input("Enter your year of study (1-4): ")
        if year in ["1", "2", "3", "4"]:
            user["year"] = year
            break
        print("Please enter a valid year between 1 and 4.")

    print("\nThank you for registering!")
    print("Your information has been recorded successfully.\n")
    return user
        
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
        if prediction == "registration":
            user = register_user()

            print("\nCollected Information:")

            for key, value in user.items():
                print(f"{key.title()}: {value}")
        