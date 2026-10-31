from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

client = genai.Client(api_key=api_key)

conversation = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        message = data.get("message")

        if not message:
            return jsonify({
                "error": "Message is required"
            }), 400

        conversation.append({
            "role": "user",
            "text": message
        })

        conversation_text = ""

        for item in conversation:
            conversation_text += (
                item["role"] + ": " + item["text"] + "\n"
            )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=conversation_text
        )

        conversation.append({
            "role": "assistant",
            "text": response.text
        })

        return jsonify({
            "response": response.text
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)