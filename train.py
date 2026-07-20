import json
import joblib
from utils.preprocess import preprocess
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

with open("data/intents.json", "r") as file:
    data = json.load(file)

patterns = []
tags = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        processed = preprocess(pattern)

        # Convert list back into sentence
        processed = " ".join(processed)

        patterns.append(processed)
        tags.append(intent["tag"])

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(patterns)

model = MultinomialNB()
model.fit(X, tags)

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained and saved successfully!")
