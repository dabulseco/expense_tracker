"""
This module handles the persistence of expenses to the filesystem.
It converts Python Expense objects to CSV rows and vice-versa,
acting as the data access layer for the application.
"""

import csv
from decimal import Decimal, InvalidOperation
from datetime import date
from typing import List
from src.models import Expense, ExpenseValidationError
from src.utils import parse_date

class CSVHandler:
    """
    Handles the persistence of Expense objects to a CSV file.

    Design Choice: CSV was chosen for simplicity, human-readability, and
    ubiquity. It allows users to open their data in spreadsheet software.

    Assumption: The dataset is small enough to be loaded entirely into
    memory (RAM) as a list of Python objects.
    """
    # Schema Definition: Fixed order of columns ensures consistency across save/load.
    FIELDNAMES = ["amount", "category", "description", "date"]

    def __init__(self, filename: str = "expenses.csv"):
        # Assumption: We use UTF-8 encoding to ensure cross-platform compatibility.
        self.filename = filename

    def save(self, expenses: List[Expense]):
        """
        Writes a list of Expense objects to the main CSV file.
        This is a convenience wrapper around save_to_custom_file.
        """
        self.save_to_custom_file(expenses, self.filename)

    def save_to_custom_file(self, expenses: List[Expense], filename: str):
        """
        Writes a list of Expense objects to a specified CSV file.
        Used for both the main database and for exporting filtered results.
        """
        try:
            # Open file in write mode ('w') with newline='' as required by the csv module
            with open(filename, mode="w", newline="", encoding="utf-8") as f:
                # DictWriter allows us to use dictionaries to map data to columns
                writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)

                # Write the header row (column names) first
                writer.writeheader()

                # Iterate through each Expense object and convert its attributes to strings
                for exp in expenses:
                    writer.writerow({
                        "amount": str(exp.amount),
                        "category": exp.category,
                        "description": exp.description,
                        "date": exp.date.isoformat() # Convert date object to YYYY-MM-DD string
                    })
        except IOError as e:
            print(f"Error saving to file {filename}: {e}")
            raise

    def load(self) -> List[Expense]:
        """
        Reads the CSV file and converts each row into an Expense object.

        Design Choice: 'Ingestion Validation' is implemented here to catch errors
        introduced by manual file editing, preventing the application from crashing.
        """
        expenses = []
        try:
            # Open file in read mode ('r')
            with open(self.filename, mode="r", newline="", encoding="utf-8") as f:
                # DictReader treats the first row as field names and subsequent rows as dictionaries
                reader = csv.DictReader(f)

                # We track the row index for better error messages (start=2 because row 1 is header)
                for row_idx, row in enumerate(reader, start=2):
                    try:
                        # 1. Validate amount separately to provide a row-specific error message.
                        try:
                            amount = Decimal(row["amount"])
                        except (InvalidOperation, KeyError):
                            raise ExpenseValidationError(f"Invalid amount at row {row_idx}")

                        # 2. Validate date using our normalization utility.
                        parsed_date = parse_date(row.get("date", ""))
                        if parsed_date is None:
                            raise ExpenseValidationError(f"Invalid date at row {row_idx}")

                        # 3. Create Expense object (this triggers the model's internal validation).
                        exp = Expense(
                            amount=amount,
                            category=row.get("category", ""),
                            description=row.get("description", ""),
                            date=parsed_date
                        )
                        expenses.append(exp)
                    except ExpenseValidationError as e:
                        # Assumption: If a row is corrupted, we skip it rather than
                        # failing the entire load, prioritizing availability of valid data.
                        print(f"Skipping corrupted row {row_idx}: {e}")
                        continue
        except FileNotFoundError:
            # Assumption: A missing file is not an error, but represents a fresh start.
            return []
        except IOError as e:
            print(f"Error reading file {self.filename}: {e}")
            raise

        return expenses
