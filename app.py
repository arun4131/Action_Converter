from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# 🔑 Replace with your NEW API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.route("/")
def home():
    return "Backend is running"


@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.json

    user_input = data.get("input")
    time = data.get("time")

    if not user_input or not time:
        return jsonify({"error": "Missing input or time"}), 400

    try:
        # 🧠 Prompt
        prompt = f"""
You are an expert learning coach.

Convert the user’s goal into a VERY SIMPLE actionable plan.

User goal: {user_input}
Available time per day: {time} hours

Rules:
- Maximum 5 days only
- Each day must have 1 clear action
- Keep each step SHORT (1 line only)
- Focus on doing, not theory
- No long explanations

Output format:
Day 1: ...
Day 2: ...
Day 3: ...
Day 4: ...
Day 5: ...
"""


        # 🔥 Working Groq model (latest)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        plan = response.choices[0].message.content

        return jsonify({"plan": plan})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)