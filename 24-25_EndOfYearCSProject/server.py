from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Allows our HTML frontend to access this API

# MongoDB connection 
client = MongoClient("mongodb+srv://<username>:<password>@<cluster-url>/test?retryWrites=true&w=majority") < #Replace with our MongoDB info
db = client["friend_matcher"]
collection = db[""] < #Replace with our collection name

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    name = data.get("name")
    age = int(data.get("age"))
    interests = [i.strip() for i in data.get("interests", "").split(",")]

    new_user = {"name": name, "age": age, "interests": interests}
    collection.insert_one(new_user)
    
    return jsonify({"message": "User added successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
