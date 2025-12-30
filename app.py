from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import wikipedia
import os

app = Flask(__name__)
CORS(app)

wikipedia.set_lang("en")

OPENAI_API_KEY = os.getenv("OPEN_API_KEY_HERE")

@app.route("/")
def home():
    return jsonify({"status": "Smart AI Browser Backend Running"})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query missing"}), 400

    # ---------- TRY WIKIPEDIA ----------
    wiki_result = None
    try:
        wiki_result = wikipedia.summary(query, sentences=2)
    except:
        pass

    # ---------- TRY CHATGPT ----------
    gpt_result = None
    try:
        if OPENAI_API_KEY:
            res = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "user", "content": query}
                    ]
                }
            )
            gpt_result = res.json()["choices"][0]["message"]["content"]
    except:
        pass

    return jsonify({
        "wikipedia": wiki_result,
        "chatgpt": gpt_result
    })


if __name__ == "__main__":
    app.run()
