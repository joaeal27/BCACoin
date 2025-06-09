# Server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from AI import get_matches 
import certifi
app = Flask(__name__)
CORS(app)  # permits CORS so HTML/JS can call this API from localhost


# ─── MONGODB CONNECTION ────────────────────────────────────────────────────────
MONGO_URI = (
    "mongodb+srv://ryanarumemi08:endofyear2025"
    "@cluster0.hrlavhw.mongodb.net/"
    "?retryWrites=true&w=majority&appName=Cluster0"
)
client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())

db = client["friend_matcher"]
collection = db["users"]


# ─── POST /add_user ─────────────────────────────────────────────────────────────
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    age_raw = data.get("age", "").strip()
    interests_raw = data.get("interests", "")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    try:
        age = int(age_raw)
        if age < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Age must be a non‐negative integer"}), 400

    interests = [i.strip() for i in interests_raw.split(",") if i.strip()]

    new_user = {"name": name, "age": age, "interests": interests}
    try:
        collection.insert_one(new_user)
    except Exception as e:
        return jsonify({"error": f"Failed to insert into DB: {e}"}), 500

  
    all_users = list(collection.find({}, {"_id": 0}))
    return jsonify({"message": "User added successfully", "users": all_users}), 200


# ─── GET /users ─────────────────────────────────────────────────────────────────
@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = list(collection.find({}, {"_id": 0}))
    except Exception as e:
        return jsonify({"error": f"Failed to fetch from DB: {e}"}), 500
    return jsonify(users), 200


# ─── GET /matches ──────────────────────────────────────────────────────────────
@app.route("/matches", methods=["GET"])
def matches():
    """
    Calls AI.get_matches(), which fetches all users and computes friend scores.
    Returns a JSON array of:
      [
        {
          "person": "Alice",
          "best_matches": [ ["Bob", 0.73], ["Cara", 0.28], … ]
        },
        …
      ]
    """
    try:
        results = get_matches()
    except Exception as e:
        return jsonify({"error": f"Error computing matches: {e}"}), 500

    return jsonify(results), 200


# ─── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
 
    app.run(host="0.0.0.0", port=5000, debug=True)
