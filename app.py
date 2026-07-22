from flask import Flask, render_template, request, jsonify
import json
import random
import joblib
import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        college TEXT,
        course TEXT
    )
    """)

    conn.commit()
    conn.close()

registration_state = {}

registration_data = {}

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
    user_input = request.json["message"]
    if user_input.lower() in [
    "register",
    "registration",
    "register me",
    "i want to register",
    "start registration"]:
        registration_state["step"] = "name"
        registration_data.clear()
        return jsonify({"response": "Great! Let's begin.\nWhat is your full name?"})
    
    if registration_state.get("step") == "name":
        registration_data["name"] = user_input
        registration_state["step"] = "email"
        return jsonify({"response": "Please enter your email address."})
    
    if registration_state.get("step") == "email":
        registration_data["email"] = user_input
        registration_state["step"] = "phone"
        return jsonify({"response": "Enter your phone number."})
    
    if registration_state.get("step") == "phone":
        registration_data["phone"] = user_input
        registration_state["step"] = "college"
        return jsonify({
        "response": "Which college do you study in?"
    })
        
    if registration_state.get("step") == "college":   
        registration_data["college"] = user_input
        registration_state["step"] = "course"
        return jsonify({"response": "Which course are you pursuing?"})
    
    if registration_state.get("step") == "course":
        registration_data["course"] = user_input
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO registrations
                       (name,email,phone,college,course)
                       VALUES (?,?,?,?,?)
                       """,
                       (
                           registration_data["name"],
                           registration_data["email"],
                           registration_data["phone"],
                           registration_data["college"],
                           registration_data["course"]
                        ))
        conn.commit()
        conn.close()
        registration_state["step"] = None
        return jsonify({"response": f"Registration Complete!\n\n"
            f"Name: {registration_data['name']}\n"
            f"Email: {registration_data['email']}\n"
            f"Phone: {registration_data['phone']}\n"
            f"College: {registration_data['college']}\n"
            f"Course: {registration_data['course']}"})

    processed = preprocess(user_message)
    processed = " ".join(processed)

    vector = vectorizer.transform([processed])

    prediction = model.predict(vector)[0]

    response = get_response(prediction)

    return jsonify({"response": response})

@app.route("/admin")
def admin():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM registrations")

    registrations = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        registrations=registrations
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)