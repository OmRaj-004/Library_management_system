# Library Management System

A pure Python mini project for managing a library. It stores data locally in a JSON file and does not require PostgreSQL, MySQL, SQLite, or any external database.

## Features

- Add, update, search, and list books
- Register and list members
- Issue books only when copies are available
- Return books and calculate late fines
- Track total, issued, and available book copies
- View currently issued books
- View overdue books and estimated fines
- Record fine payments

## Tech Stack

- Python 3.10+
- JSON file storage using the Python standard library

## Project Structure

```text
Library_Management_System/
  src/library_management/
    cli.py
    services.py
    storage.py
  data/
    library_data.json      # created automatically on first run
  docs/
    project_report.md
  requirements.txt         # no external packages required
  README.md
```

## How Data Is Stored

The application uses:

```text
data/library_data.json
```

If the file does not exist, the program creates it automatically with sample books, members, and issue records.

## Run the Project

From the project folder:

```bash
python -m src.library_management.cli
```

No dependency installation is required.

## Main Modules

- `cli.py`: Menu-driven command-line interface
- `services.py`: Business logic for books, members, issue/return, fines, and availability
- `storage.py`: JSON file loading, saving, and sample-data initialization

## Fine Rule

The fine is currently:

```text
5 per late day
```

It is configured in `src/library_management/services.py` as `FINE_PER_DAY`.

## Availability Rule

```text
available_copies = total_copies - issued_copies
```

Only issue records with status `ISSUED` are counted as issued copies.

