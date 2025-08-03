from flask import Flask, request, jsonify
import joblib
import os
import re

app = Flask(__name__)

# Load the trained model
model = joblib.load('model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Basic clean-up function
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

@app.route('/')
def home():
    return "Scam Screener API is running."

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    processed = preprocess(message)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)[0]

    result = "Likely Scam" if prediction == 1 else "Likely Legitimate"
    return jsonify({"prediction": result})
