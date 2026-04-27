from decimal import Decimal

from . import services


def prompt_int(label):
    while True:
        value = input(label).strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid number.")


def prompt_decimal(label):
    while True:
        value = input(label).strip()
        try:
            return Decimal(value)
        except Exception:
            print("Please enter a valid amount.")


def print_rows(rows):
    if not rows:
        print("No records found.")
        return

    headers = list(rows[0].keys())
    widths = {
        header: max(len(str(header)), *(len(str(row[header])) for row in rows))
        for header in headers
    }
    header_line = " | ".join(str(header).ljust(widths[header]) for header in headers)
    separator = "-+-".join("-" * widths[header] for header in headers)
    print(header_line)
    print(separator)
    for row in rows:
        print(" | ".join(str(row[header]).ljust(widths[header]) for header in headers))


def add_book_menu():
    isbn = input("ISBN: ").strip()
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    publisher = input("Publisher: ").strip() or None
    category = input("Category: ").strip() or None
    year_text = input("Publication year: ").strip()
    publication_year = int(year_text) if year_text else None
    total_copies = prompt_int("Total copies: ")
    book_id = services.add_book(isbn, title, author, publisher, category, publication_year, total_copies)
    print(f"Book added with ID {book_id}.")


def update_book_copies_menu():
    book_id = prompt_int("Book ID: ")
    total_copies = prompt_int("New total copies: ")
    result = services.update_book_copies(book_id, total_copies)
    print("Book copies updated." if result else "Book not found.")


def add_member_menu():
    full_name = input("Full name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip() or None
    address = input("Address: ").strip() or None
    member_id = services.add_member(full_name, email, phone, address)
    print(f"Member registered with ID {member_id}.")


def issue_book_menu():
    book_id = prompt_int("Book ID: ")
    member_id = prompt_int("Member ID: ")
    loan_days_text = input("Loan days [14]: ").strip()
    loan_days = int(loan_days_text) if loan_days_text else services.DEFAULT_LOAN_DAYS
    issue_id = services.issue_book(book_id, member_id, loan_days)
    print(f"Book issued. Issue ID: {issue_id}.")


def return_book_menu():
    issue_id = prompt_int("Issue ID: ")
    result = services.return_book(issue_id)
    print(f"Book returned. Fine amount: {result['fine_amount']}.")


def search_books_menu():
    keyword = input("Search keyword: ").strip()
    print_rows(services.search_books(keyword))


def fine_payment_menu():
    issue_id = prompt_int("Issue ID: ")
    paid_amount = prompt_decimal("Paid amount: ")
    payment_id = services.record_fine_payment(issue_id, paid_amount)
    print(f"Fine payment recorded with ID {payment_id}.")


def show_menu():
    print()
    print("Library Management System")
    print("1. Add book")
    print("2. List books with availability")
    print("3. Search books")
    print("4. Update book copies")
    print("5. Register member")
    print("6. List members")
    print("7. Issue book")
    print("8. Return book")
    print("9. List issued books")
    print("10. List overdue books")
    print("11. Record fine payment")
    print("0. Exit")


def main():
    actions = {
        "1": add_book_menu,
        "2": lambda: print_rows(services.list_books()),
        "3": search_books_menu,
        "4": update_book_copies_menu,
        "5": add_member_menu,
        "6": lambda: print_rows(services.list_members()),
        "7": issue_book_menu,
        "8": return_book_menu,
        "9": lambda: print_rows(services.list_issued_books()),
        "10": lambda: print_rows(services.list_overdue_books()),
        "11": fine_payment_menu,
    }

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break

        action = actions.get(choice)
        if action is None:
            print("Invalid option.")
            continue

        try:
            action()
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
