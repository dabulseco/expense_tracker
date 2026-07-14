"""
Unit tests for the Tracker business logic layer.
These tests verify that expenses are correctly managed in memory,
category totals are accurately aggregated, and that the Tracker
correctly interfaces with the Storage layer.
"""

import unittest
from decimal import Decimal
from datetime import date
from src.models import Expense
from src.storage import CSVHandler
from src.tracker import Tracker

class TestTracker(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for storage testing to avoid overwriting real data
        self.test_file = "test_tracker_expenses.csv"
        self.storage = CSVHandler(self.test_file)
        self.tracker = Tracker(self.storage)

    def tearDown(self):
        # Clean up the temporary file after each test
        import os
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_and_get_expenses(self):
        """Verify that expenses can be added to the tracker and retrieved as a list."""
        exp1 = Expense(amount=Decimal("10.00"), category="Food", description="Lunch", date=date.today())
        exp2 = Expense(amount=Decimal("20.00"), category="Transport", description="Taxi", date=date.today())

        self.tracker.add_expense(exp1)
        self.tracker.add_expense(exp2)

        # Verify the count and that the specific objects were stored
        self.assertEqual(len(self.tracker.get_all_expenses()), 2)
        self.assertIn(exp1, self.tracker.get_all_expenses())
        self.assertIn(exp2, self.tracker.get_all_expenses())

    def test_category_aggregation(self):
        """Verify that the Tracker correctly sums expenses grouped by category."""
        # Add multiple expenses in the same category to test summation
        self.tracker.add_expense(Expense(amount=Decimal("10.00"), category="Food", description="Lunch", date=date.today()))
        self.tracker.add_expense(Expense(amount=Decimal("5.00"), category="Food", description="Snack", date=date.today()))
        self.tracker.add_expense(Expense(amount=Decimal("20.00"), category="Transport", description="Taxi", date=date.today()))

        totals = self.tracker.get_category_totals()

        # Food should be 10 + 5 = 15
        self.assertEqual(totals["Food"], Decimal("15.00"))
        # Transport should be 20
        self.assertEqual(totals["Transport"], Decimal("20.00"))

    def test_storage_bridge(self):
        """Verify that save_to_disk and load_from_disk correctly persist the tracker state."""
        exp = Expense(amount=Decimal("10.00"), category="Food", description="Lunch", date=date.today())
        self.tracker.add_expense(exp)

        # Act: Save the current state to disk
        self.tracker.save_to_disk()

        # Simulate application restart by creating a fresh tracker instance
        # that points to the same physical file.
        new_tracker = Tracker(self.storage)
        new_tracker.load_from_disk()

        # Assert: The new tracker should have recovered the saved data
        self.assertEqual(len(new_tracker.get_all_expenses()), 1)
        self.assertEqual(new_tracker.get_all_expenses()[0].amount, Decimal("10.00"))

if __name__ == "__main__":
    unittest.main()
