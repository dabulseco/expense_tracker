# Personal Expense Tracker

A robust, command-line application built with Python 3.11 to help users track their daily expenses with a focus on data integrity and precision.

> **Note:** This project was developed as a classroom exercise as part of a coding course to practice software engineering principles, including data validation, dependency injection, and persistent storage.

## 🚀 Features

- **Validated Data Entry:** Prevents "bad data" (e.g., negative amounts or invalid dates) from entering the system using a multi-layer validation strategy.
- **Financial Precision:** Uses the `decimal` library instead of floating-point numbers to avoid rounding errors common in monetary calculations.
- **Category Reporting:** Quickly view total spending grouped by category.
- **Advanced Filtering:** Search for expenses by category with case-insensitive matching.
- **Custom Exports:** Filter expenses by category and export the resulting list to a separate CSV file for use in other applications.
- **Automatic Persistence:** Expenses are automatically loaded from disk on startup and saved upon exiting the application.

## 🛠️ Technical Stack

- **Language:** Python 3.11
- **Storage:** CSV (Comma Separated Values)
- **Key Libraries:** `dataclasses`, `csv`, `datetime`, `decimal`

## 📂 Project Structure

- `src/main.py`: The entry point and composition root of the application.
- `src/cli.py`: Handles user interaction and the menu loop.
- `src/tracker.py`: Contains the business logic for managing and filtering expenses.
- `src/storage.py`: Manages reading and writing data to the filesystem.
- `src/models.py`: Defines the `Expense` data model and validation rules.
- `src/utils.py`: Shared utility functions (e.g., date parsing).
- `tests/`: A comprehensive suite of unit and integration tests.

## 🚦 Getting Started

### Prerequisites
- Python 3.11 or higher installed on your system.

### Running the Application
1. Clone this repository or navigate to the project folder.
2. Run the application using the following command:
   ```bash
   python3 -m src.main
   ```

### Running Tests
To verify the application's logic, you can run the test suite:
```bash
python3 -m unittest discover tests
```

## 📝 How it Works
The application follows a layered architecture to separate concerns:
1. **UI Layer (`CLI`)** $\rightarrow$ captures user input and displays data.
2. **Logic Layer (`Tracker`)** $\rightarrow$ processes data and handles calculations.
3. **Storage Layer (`CSVHandler`)** $\rightarrow$ manages physical file I/O.
4. **Model Layer (`Expense`)** $\rightarrow$ ensures every record is logically valid.
