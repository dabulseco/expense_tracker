"""
Unit tests for the CSVHandler storage layer.
These tests ensure that data is correctly persisted to disk and that
corrupted data in the CSV file is handled gracefully without crashing the app.
"""

import unittest
import os
from decimal import Decimal
from datetime import date
from src.models import Expense
from src.storage import CSVHandler

class TestCSVHandler(unittest.TestCase):
    def setUp(self):
        """Prepare a fresh test file and a set of sample data before each test."""
        self.test_file = "test_expenses.csv"
        self.handler = CSVHandler(self.test_file)
        self.sample_expenses = [
            Expense(amount=Decimal("10.50"), category="Food", description="Lunch", date=date(2023, 1, 1)),
            Expense(amount=Decimal("20.00"), category="Transport", description="Taxi", date(date(2023, 1, 2))),
        ]

    def tearDown(self):
        """Clean up the test file after each test to avoid side effects."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_round_trip(self):
        """Verify that saving and loading expenses results in the exact same data."""
        # Act: Save the sample list and load it back
        self.handler.save(self.sample_expenses)
        loaded_expenses = self.handler.load()

        # Assert: The length and every attribute of the objects should match
        self.assertEqual(len(loaded_expenses), len(self.sample_expenses))
        for original, loaded in zip(self.sample_expenses, loaded_expenses):
            self.assertEqual(original.amount, loaded.amount)
            self.assertEqual(original.category, loaded.category)
            self.assertEqual(original.description, loaded.description)
            self.assertEqual(original.date, loaded.date)

    def test_load_missing_file(self):
        """Verify that loading a non-existent file returns an empty list instead of crashing."""
        handler = CSVHandler("non_existent.csv")
        self.assertEqual(handler.load(), [])

    def test_corrupted_data_handling(self):
        """Verify that the loader skips rows with invalid data (Ingestion Validation)."""
        # Manually create a corrupted CSV to test resilience
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("amount,category,description,date\n")
            f.write("10.50,Food,Lunch,2023-01-01\n") # Valid
            f.write("not_a_number,Food,Lunch,2023-01-02\n") # Invalid amount (non-numeric)
            f.write("20.00,Transport,Taxi,invalid-date\n") # Invalid date (wrong format)
            f.write("0.00,Food,Lunch,2023-01-03\n") # Invalid amount (non-positive)
            f.write("30.00,Transport,Ride,2023-01-04\n") # Valid

        # Act: Load the file containing corrupted rows
        loaded = self.handler.load()

        # Assert: Only the 2 valid rows should have been loaded into the system
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].amount, Decimal("10.50"))
        self.assertEqual(loaded[1].amount, Decimal("30.00"))

if __name__ == "__main__":
    unittest.main()
