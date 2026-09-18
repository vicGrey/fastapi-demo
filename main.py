from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI()

mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)

db = client["testdb"]
users = db["users"]

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/users")
def create_user(name: str):
    result = users.insert_one({"name": name})

    return {
        "message": "user created",
        "id": str(result.inserted_id)
    }

@app.get("/users")
def get_users():
    return list(users.find({}, {"_id": 0    }))

@app.get("/health")
def health_check():
    return {"message": "Docker is starting to make sense"}