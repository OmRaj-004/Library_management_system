import json
from copy import deepcopy
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "library_data.json"


DEFAULT_DATA = {
    "next_ids": {
        "book_id": 6,
        "member_id": 4,
        "issue_id": 3,
        "payment_id": 1,
    },
    "books": [
        {
            "book_id": 1,
            "isbn": "9780134685991",
            "title": "Effective Java",
            "author": "Joshua Bloch",
            "publisher": "Addison-Wesley",
            "category": "Programming",
            "publication_year": 2018,
            "total_copies": 4,
        },
        {
            "book_id": 2,
            "isbn": "9780132350884",
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "publisher": "Prentice Hall",
            "category": "Programming",
            "publication_year": 2008,
            "total_copies": 3,
        },
        {
            "book_id": 3,
            "isbn": "9780262033848",
            "title": "Introduction to Algorithms",
            "author": "Cormen, Leiserson, Rivest, Stein",
            "publisher": "MIT Press",
            "category": "Computer Science",
            "publication_year": 2009,
            "total_copies": 2,
        },
        {
            "book_id": 4,
            "isbn": "9789353165130",
            "title": "Database System Concepts",
            "author": "Silberschatz, Korth, Sudarshan",
            "publisher": "McGraw Hill",
            "category": "Database",
            "publication_year": 2019,
            "total_copies": 5,
        },
        {
            "book_id": 5,
            "isbn": "9788173711466",
            "title": "Let Us C",
            "author": "Yashavant Kanetkar",
            "publisher": "BPB Publications",
            "category": "Programming",
            "publication_year": 2016,
            "total_copies": 6,
        },
    ],
    "members": [
        {
            "member_id": 1,
            "full_name": "Aarav Sharma",
            "email": "aarav.sharma@example.com",
            "phone": "9876543210",
            "address": "Delhi",
            "membership_date": "2026-04-22",
            "is_active": True,
        },
        {
            "member_id": 2,
            "full_name": "Priya Nair",
            "email": "priya.nair@example.com",
            "phone": "9876543211",
            "address": "Kochi",
            "membership_date": "2026-04-22",
            "is_active": True,
        },
        {
            "member_id": 3,
            "full_name": "Rahul Mehta",
            "email": "rahul.mehta@example.com",
            "phone": "9876543212",
            "address": "Mumbai",
            "membership_date": "2026-04-22",
            "is_active": True,
        },
    ],
    "issue_records": [
        {
            "issue_id": 1,
            "book_id": 1,
            "member_id": 1,
            "issue_date": "2026-04-19",
            "due_date": "2026-05-03",
            "return_date": None,
            "fine_amount": "0.00",
            "status": "ISSUED",
        },
        {
            "issue_id": 2,
            "book_id": 4,
            "member_id": 2,
            "issue_date": "2026-04-02",
            "due_date": "2026-04-16",
            "return_date": None,
            "fine_amount": "0.00",
            "status": "ISSUED",
        },
    ],
    "fine_payments": [],
}


def load_data():
    if not DATA_FILE.exists():
        save_data(deepcopy(DEFAULT_DATA))

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def next_id(data, key):
    value = data["next_ids"][key]
    data["next_ids"][key] += 1
    return value
