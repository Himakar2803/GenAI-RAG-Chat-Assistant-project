from flask import Flask, render_template, request, jsonify
import json
import numpy as np
import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# Gemini API key
genai.configure(api_key="AIzaSyBhqsqB8XZZHhKb6CzVE1RtzWlpt9dIyJw")

# Load documents
with open("docs.json") as f:
    documents = json.load(f)

# Simple embedding function
def generate_embedding(text):
    return np.array([ord(c) for c in text[:100]])

# Store embeddings
embeddings = []
texts = []

for doc in documents:
    emb = generate_embedding(doc["content"])
    embeddings.append(emb)
    texts.append(doc["content"])

# Search similar documents
def search(query):

    query_emb = generate_embedding(query)

    sims = []

    for emb in embeddings:
        min_len = min(len(query_emb), len(emb))

        sims.append(
            cosine_similarity(
                [query_emb[:min_len]],
                [emb[:min_len]]
            )[0][0]
        )

    top = np.argsort(sims)[-3:][::-1]

    context = ""

    for i in top:
        context += texts[i] + "\n"

    return context


# Generate AI response
def get_response(context, query):

    prompt = f"""
Answer using the following context:

{context}

User Question: {query}
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if response.text:
            return response.text
        else:
            return "AI did not return a response."

    except Exception as e:
        print("Gemini Error:", e)
        return "AI service temporarily unavailable."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:
        user = request.json["message"]

        context = search(user)

        reply = get_response(context, user)

        return jsonify({"reply": reply})

    except Exception as e:
        print("Server Error:", e)
        return jsonify({"reply": "Server error occurred."})


# IMPORTANT FOR RENDER DEPLOYMENT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
