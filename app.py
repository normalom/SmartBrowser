from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def home():
    return "SmartBrowser Backend Running!"

@app.route("/ask", methods=["POST"])
def ask_ai():
    data = request.get_json()
    user_input = data.get("query", "")

    if not user_input:
        return jsonify({"error": "Query missing"}), 400

    return jsonify({
        "reply": f"You said: {user_input}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
