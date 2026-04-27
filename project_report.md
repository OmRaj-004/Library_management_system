# Library Management System - Python Project Report

## Objective

The objective of this project is to implement a Library Management System using pure Python. The system manages books, members, issue and return records, late-return fines, and book availability without using an external database.

## Scope

The system supports the following operations:

- Store book details such as ISBN, title, author, category, and number of copies
- Store member details such as name, email, phone, and address
- Issue books to active members
- Return issued books
- Calculate fines for late returns
- Track total, issued, and available book copies
- View overdue records
- Record fine payments

## Data Storage

The project uses a local JSON file:

```text
data/library_data.json
```

This file is created automatically on the first run. It stores books, members, issue records, fine payments, and the next available ID values.

## Main Components

### Books

Stores book information:

- book ID
- ISBN
- title
- author
- publisher
- category
- publication year
- total copies

### Members

Stores library member information:

- member ID
- full name
- email
- phone
- address
- membership date
- active status

### Issue Records

Stores book issue and return transactions:

- issue ID
- book ID
- member ID
- issue date
- due date
- return date
- fine amount
- status

### Fine Payments

Stores payment records for fines:

- payment ID
- issue ID
- paid amount
- paid date

## Validation Rules

- ISBN must be unique
- Member email must be unique
- Total copies cannot be negative
- A book cannot be issued if no copies are available
- A returned issue record cannot be returned again
- Fine payment cannot be recorded for a missing issue record
- Total copies cannot be reduced below the number of currently issued copies

## Fine Calculation

When a book is returned, the system compares the current date with the due date.

```text
late_days = max(return_date - due_date, 0)
fine_amount = late_days * fine_per_day
```

The current fine rate is `5` per late day.

## Availability Tracking

The system calculates availability dynamically:

```text
issued_copies = count of issue records where status is ISSUED
available_copies = total_copies - issued_copies
```

## Conclusion

This project demonstrates file handling, structured data storage, menu-driven programming, validation, date handling, and business logic implementation using only Python.
