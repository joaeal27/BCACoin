# AI.py
from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient

# ─── MONGODB SETUP ──────────────────────────────────────────────────────────────
MONGO_URI = (
    "mongodb+srv://ryanarumemi08:endofyear2025"
    "@cluster0.hrlavhw.mongodb.net/"
    "?retryWrites=true&w=majority&appName=Cluster0"
)
client = MongoClient(MONGO_URI)
db = client["friend_matcher"]
collection = db["users"]


# ─── CORE LOGIC ─────────────────────────────────────────────────────────────────
def interest_similarity_matrix(people: List[Dict]) -> np.ndarray:
    """
    Given a list of people (each with an 'interests' list), return
    the cosine‐similarity matrix on their interest vectors.
    """
    interest_strings = [" ".join(person["interests"]) for person in people]
    vectorizer = CountVectorizer().fit_transform(interest_strings)
    return cosine_similarity(vectorizer)


def age_similarity(age1: int, age2: int) -> float:
    """
    Simple age similarity: 1 / (1 + |age1 − age2|).
    Closer ages produce a higher score in (0, 1].
    """
    return 1.0 / (1.0 + abs(age1 - age2))


def compute_friend_scores(people: List[Dict]) -> List[Dict]:
    """
    Given a list of {name, age, interests}, compute for each person
    a sorted list of (other_name, total_score).
    Returns a list of dicts: 
      [
        { "person": "Alice", "best_matches": [("Bob", 0.73), ("Cara", 0.28), …] },
        { "person": "Bob", … },
        ...
      ]
    """
    interest_sim = interest_similarity_matrix(people)
    results = []

    for i, person in enumerate(people):
        scores = []
        for j, other in enumerate(people):
            if i == j:
                continue
            age_score = age_similarity(person["age"], other["age"])
            interest_score = float(interest_sim[i][j])
            total_score = 0.5 * age_score + 0.5 * interest_score
            scores.append((other["name"], total_score))

        # Sort descending by total_score
        scores.sort(key=lambda x: x[1], reverse=True)
        results.append({"person": person["name"], "best_matches": scores})

    return results


def get_matches() -> List[Dict]:
    """
    Fetch all users from MongoDB (excluding Mongo’s _id), then
    compute & return friend‐matching scores.
    """
    people = list(collection.find({}, {"_id": 0}))
    if not people:
        return []  # No users => no matches
    return compute_friend_scores(people)


# If you ever run AI.py directly, we could print to console (optional)
if __name__ == "__main__":
    matches = get_matches()
    for match in matches:
        print(f"\n{match['person']}'s top matches:")
        for name, score in match["best_matches"]:
            print(f"  {name} — Score: {score:.2f}")
