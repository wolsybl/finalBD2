"""MongoDB access and CRUD operations."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo import MongoClient, ReturnDocument

from app.config import DB_NAME, MONGO_URI


_client: Optional[MongoClient] = None


def get_db():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client[DB_NAME]


def ensure_indexes() -> None:
    db = get_db()
    db.users.create_index("email", unique=True)
    db.movies.create_index([("name", 1), ("schedule", 1)], unique=True)
    db.purchases.create_index("user_id")
    db.purchases.create_index("movie_id")


def to_object_id(value: str) -> ObjectId:
    return ObjectId(value)


# Users

def create_user(name: str, email: str, preference: str) -> str:
    db = get_db()
    doc = {
        "name": name.strip(),
        "email": email.strip().lower(),
        "preference": preference.strip(),
        "created_at": datetime.utcnow(),
    }
    result = db.users.insert_one(doc)
    return str(result.inserted_id)


def list_users() -> List[Dict[str, Any]]:
    db = get_db()
    return list(db.users.find().sort("created_at", -1))


def update_user(user_id: str, name: str, email: str, preference: str) -> bool:
    db = get_db()
    result = db.users.update_one(
        {"_id": to_object_id(user_id)},
        {"$set": {"name": name.strip(), "email": email.strip().lower(), "preference": preference.strip()}},
    )
    return result.modified_count > 0


def delete_user(user_id: str) -> bool:
    db = get_db()
    result = db.users.delete_one({"_id": to_object_id(user_id)})
    return result.deleted_count > 0


def get_user_purchases(user_id: str) -> List[Dict[str, Any]]:
    db = get_db()
    return list(db.purchases.find({"user_id": to_object_id(user_id)}).sort("purchased_at", -1))


# Movies

def create_movie(name: str, genre: str, duration: str, schedule: str, tickets: int, price: float) -> str:
    db = get_db()
    doc = {
        "name": name.strip(),
        "genre": genre.strip(),
        "duration": duration.strip(),
        "schedule": schedule.strip(),
        "available_tickets": int(tickets),
        "price": float(price),
        "created_at": datetime.utcnow(),
    }
    result = db.movies.insert_one(doc)
    return str(result.inserted_id)


def list_movies() -> List[Dict[str, Any]]:
    db = get_db()
    return list(db.movies.find().sort("created_at", -1))


def update_movie(
    movie_id: str,
    name: str,
    genre: str,
    duration: str,
    schedule: str,
    tickets: int,
    price: float,
) -> bool:
    db = get_db()
    result = db.movies.update_one(
        {"_id": to_object_id(movie_id)},
        {
            "$set": {
                "name": name.strip(),
                "genre": genre.strip(),
                "duration": duration.strip(),
                "schedule": schedule.strip(),
                "available_tickets": int(tickets),
                "price": float(price),
            }
        },
    )
    return result.modified_count > 0


def delete_movie(movie_id: str) -> bool:
    db = get_db()
    result = db.movies.delete_one({"_id": to_object_id(movie_id)})
    return result.deleted_count > 0


# Purchases

def create_purchase(user_id: str, movie_id: str, quantity: int) -> Optional[Dict[str, Any]]:
    db = get_db()
    qty = int(quantity)
    if qty <= 0:
        return None

    movie = db.movies.find_one_and_update(
        {"_id": to_object_id(movie_id), "available_tickets": {"$gte": qty}},
        {"$inc": {"available_tickets": -qty}},
        return_document=ReturnDocument.AFTER,
    )

    if movie is None:
        return None

    user = db.users.find_one({"_id": to_object_id(user_id)})
    if user is None:
        return None

    total = float(movie["price"]) * qty
    purchase = {
        "user_id": user["_id"],
        "user_name": user["name"],
        "movie_id": movie["_id"],
        "movie_name": movie["name"],
        "quantity": qty,
        "total": total,
        "purchased_at": datetime.utcnow(),
        "schedule": movie["schedule"],
    }

    result = db.purchases.insert_one(purchase)
    purchase["_id"] = result.inserted_id
    return purchase


def list_purchases() -> List[Dict[str, Any]]:
    db = get_db()
    return list(db.purchases.find().sort("purchased_at", -1))
