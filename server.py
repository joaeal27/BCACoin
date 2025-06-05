from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Allows our HTML frontend to access this API

# MongoDB connection 
client = MongoClient("mongodb%2Bsrv%3A%2F%2Fryanarumemi08%3Aendofyear2025%40cluster0.hrlavhw.mongodb.net%2F%3FretryWrites%3Dtrue%26w%3Dmajority%26appName%3DCluster0")
db = client["friend_matcher"]
collection = db["users"] 

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
    app.run(host="0.0.0.0", port=5000, debug=True)
