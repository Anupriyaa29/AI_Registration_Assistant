import json
from utils.preprocess import preprocess
from sklearn.feature_extraction.text import CountVectorizer

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

print("Vocabulary:")
print(vectorizer.vocabulary_)

print()

print("Bag of Words Matrix:")

print(X.toarray())