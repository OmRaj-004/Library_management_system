from datetime import date, timedelta
from decimal import Decimal

from .storage import load_data, next_id, save_data


DEFAULT_LOAN_DAYS = 14
FINE_PER_DAY = Decimal("5")


def fine_per_day():
    return FINE_PER_DAY


def parse_date(value):
    return date.fromisoformat(value)


def today_string():
    return date.today().isoformat()


def money(value):
    return Decimal(str(value)).quantize(Decimal("0.01"))


def find_by_id(items, key, value):
    return next((item for item in items if item[key] == value), None)


def issued_count(data, book_id):
    return sum(
        1
        for record in data["issue_records"]
        if record["book_id"] == book_id and record["status"] == "ISSUED"
    )


def book_availability_row(data, book):
    issued = issued_count(data, book["book_id"])
    return {
        "book_id": book["book_id"],
        "isbn": book["isbn"],
        "title": book["title"],
        "author": book["author"],
        "category": book["category"],
        "total_copies": book["total_copies"],
        "issued_copies": issued,
        "available_copies": book["total_copies"] - issued,
    }


def add_book(isbn, title, author, publisher, category, publication_year, total_copies):
    data = load_data()
    if any(book["isbn"] == isbn for book in data["books"]):
        raise ValueError("ISBN already exists.")
    if total_copies < 0:
        raise ValueError("Total copies cannot be negative.")

    book_id = next_id(data, "book_id")
    data["books"].append(
        {
            "book_id": book_id,
            "isbn": isbn,
            "title": title,
            "author": author,
            "publisher": publisher,
            "category": category,
            "publication_year": publication_year,
            "total_copies": total_copies,
        }
    )
    save_data(data)
    return book_id


def update_book_copies(book_id, total_copies):
    data = load_data()
    book = find_by_id(data["books"], "book_id", book_id)
    if book is None:
        return None

    current_issued = issued_count(data, book_id)
    if total_copies < current_issued:
        raise ValueError("Total copies cannot be less than currently issued copies.")

    book["total_copies"] = total_copies
    save_data(data)
    return {"book_id": book_id}


def list_books():
    data = load_data()
    rows = [book_availability_row(data, book) for book in data["books"]]
    return sorted(rows, key=lambda row: row["title"].lower())


def search_books(keyword):
    data = load_data()
    term = keyword.lower()
    rows = []
    for book in data["books"]:
        searchable = " ".join(
            str(book.get(field) or "")
            for field in ("title", "author", "isbn", "category")
        ).lower()
        if term in searchable:
            rows.append(book_availability_row(data, book))
    return sorted(rows, key=lambda row: row["title"].lower())


def add_member(full_name, email, phone, address):
    data = load_data()
    if any(member["email"].lower() == email.lower() for member in data["members"]):
        raise ValueError("Email already exists.")

    member_id = next_id(data, "member_id")
    data["members"].append(
        {
            "member_id": member_id,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "address": address,
            "membership_date": today_string(),
            "is_active": True,
        }
    )
    save_data(data)
    return member_id


def list_members():
    return sorted(load_data()["members"], key=lambda member: member["member_id"])


def issue_book(book_id, member_id, loan_days=DEFAULT_LOAN_DAYS):
    data = load_data()
    book = find_by_id(data["books"], "book_id", book_id)
    member = find_by_id(data["members"], "member_id", member_id)
    if book is None:
        raise ValueError("Book not found.")
    if member is None:
        raise ValueError("Member not found.")
    if not member["is_active"]:
        raise ValueError("Member is inactive.")
    if book["total_copies"] - issued_count(data, book_id) <= 0:
        raise ValueError("Book is not available for issue.")

    issue_date = date.today()
    due_date = issue_date + timedelta(days=loan_days)
    issue_id = next_id(data, "issue_id")
    data["issue_records"].append(
        {
            "issue_id": issue_id,
            "book_id": book_id,
            "member_id": member_id,
            "issue_date": issue_date.isoformat(),
            "due_date": due_date.isoformat(),
            "return_date": None,
            "fine_amount": "0.00",
            "status": "ISSUED",
        }
    )
    save_data(data)
    return issue_id


def return_book(issue_id):
    data = load_data()
    today = date.today()
    record = find_by_id(data["issue_records"], "issue_id", issue_id)

    if record is None:
        raise ValueError("Issue record not found.")
    if record["status"] == "RETURNED":
        raise ValueError("This book has already been returned.")

    late_days = max((today - parse_date(record["due_date"])).days, 0)
    fine_amount = fine_per_day() * Decimal(late_days)

    record["return_date"] = today.isoformat()
    record["fine_amount"] = str(money(fine_amount))
    record["status"] = "RETURNED"
    save_data(data)
    return {"issue_id": issue_id, "fine_amount": record["fine_amount"]}


def list_issued_books():
    data = load_data()
    rows = []
    for record in data["issue_records"]:
        if record["status"] != "ISSUED":
            continue
        book = find_by_id(data["books"], "book_id", record["book_id"])
        member = find_by_id(data["members"], "member_id", record["member_id"])
        rows.append(
            {
                "issue_id": record["issue_id"],
                "title": book["title"] if book else "Unknown",
                "author": book["author"] if book else "Unknown",
                "member_name": member["full_name"] if member else "Unknown",
                "issue_date": record["issue_date"],
                "due_date": record["due_date"],
                "overdue_days": max((date.today() - parse_date(record["due_date"])).days, 0),
            }
        )
    return sorted(rows, key=lambda row: row["due_date"])


def list_overdue_books():
    data = load_data()
    rows = []
    for record in data["issue_records"]:
        if record["status"] != "ISSUED":
            continue

        late_days = (date.today() - parse_date(record["due_date"])).days
        if late_days <= 0:
            continue

        book = find_by_id(data["books"], "book_id", record["book_id"])
        member = find_by_id(data["members"], "member_id", record["member_id"])
        rows.append(
            {
                "issue_id": record["issue_id"],
                "title": book["title"] if book else "Unknown",
                "member_name": member["full_name"] if member else "Unknown",
                "due_date": record["due_date"],
                "late_days": late_days,
                "estimated_fine": str(money(fine_per_day() * Decimal(late_days))),
            }
        )
    return sorted(rows, key=lambda row: row["due_date"])


def record_fine_payment(issue_id, paid_amount):
    data = load_data()
    if find_by_id(data["issue_records"], "issue_id", issue_id) is None:
        raise ValueError("Issue record not found.")

    payment_id = next_id(data, "payment_id")
    data["fine_payments"].append(
        {
            "payment_id": payment_id,
            "issue_id": issue_id,
            "paid_amount": str(money(paid_amount)),
            "paid_on": today_string(),
        }
    )
    save_data(data)
    return payment_id
