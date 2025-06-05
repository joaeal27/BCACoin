
import sys
sys.path.append('/path/to/scikit-learn')
import sklearn
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


####################################################################################
from pymongo import MongoClient

client = MongoClient("mongodb+srv://ryanarumemi08:endofyear2025@cluster0.hrlavhw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Select your database and collection
db = client['friend_matcher']
collection = db['users']


##################################################################################
people = [
    {"name": "Alice", "age": 36, "interests": ["music", "gaming", "reading"]},
    {"name": "Bob", "age": 27, "interests": ["music", "sports", "movies"]},
    {"name": "Cara", "age": 26, "interests": ["reading", "gaming", "coding"]},
    {"name": "Dan", "age": 25, "interests": ["music", "traveling", "photography"]},
]

# Insert the list into the collection
collection.insert_many(people)


###################################################################################
# Vectorize interests for similarity
def interest_similarity_matrix(people: List[Dict]) -> np.ndarray:
    interest_strings = [" ".join(person["interests"]) for person in people]
    vectorizer = CountVectorizer().fit_transform(interest_strings)
    return cosine_similarity(vectorizer)


###################################################################################
# Age similarity score (closer ages = higher score)
def age_similarity(age1: int, age2: int) -> float:
    return 1 / (1 + abs(age1 - age2))  # closer age = higher score


###################################################################################
# Combine interest + age similarity
def compute_friend_scores(people: List[Dict]) -> List[Dict]:
    interest_sim = interest_similarity_matrix(people)
    results = []

    for i, person in enumerate(people):
        scores = []
        for j, other in enumerate(people):
            if i == j:
                continue
            age_score = age_similarity(person["age"], other["age"])
            interest_score = interest_sim[i][j]
            total_score = 0.5 * age_score + 0.5 * interest_score  # weighted average
            scores.append((other["name"], total_score))

        scores.sort(key=lambda x: x[1], reverse=True)
        results.append({"person": person["name"], "best_matches": scores})

    return results


###################################################################################
# Load people from MongoDB
people = list(collection.find({}, {"_id": 0}))
# Display matches
matches = compute_friend_scores(people)
for match in matches:
    print(f"\n{match['person']}'s top matches:")
    for name, score in match["best_matches"]:
        print(f"  {name} — Score: {score:.2f}")
  
        
####################################################################################
