"""
Integration tests for the Personal Expense Tracker.
These tests verify that the components (Model, Storage, and Tracker) work
together as a complete system, simulating real-world user workflows
and stress-testing edge cases.
"""

import unittest
import os
from decimal import Decimal
from src.storage import CSVHandler
from src.tracker import Tracker

class TestIntegration(unittest.TestCase):
    def setUp(self):
        """Initialize a clean environment for integration tests."""
        self.filename = "integration_expenses.csv"
        self.storage = CSVHandler(self.filename)
        self.tracker = Tracker(self.storage)

    def tearDown(self):
        """Ensure the temporary integration file is deleted after tests."""
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_full_workflow(self):
        """
        Test end-to-end flow: Add -> Save -> New Tracker -> Load -> Verify.
        This simulates a user adding data, closing the app, and reopening it.
        """
        from src.models import Expense
        from datetime import date

        # 1. Add expenses to the current session
        exp1 = Expense(amount=Decimal("15.00"), category="Food", description="Coffee", date=date(2023, 1, 1))
        exp2 = Expense(amount=Decimal("50.00"), category="Utilities", description="Internet", date=date(2023, 1, 2))
        self.tracker.add_expense(exp1)
        self.tracker.add_expense(exp2)

        # 2. Save the session to disk
        self.tracker.save_to_disk()

        # 3. Simulate application restart by creating a brand new Tracker instance
        # using the same storage handler (pointing to the same file).
        new_tracker = Tracker(self.storage)
        new_tracker.load_from_disk()

        # 4. Verify that the recovered state matches the original input
        self.assertEqual(len(new_tracker.get_all_expenses()), 2)
        self.assertEqual(new_tracker.get_category_totals()["Food"], Decimal("15.00"))
        self.assertEqual(new_tracker.get_category_totals()["Utilities"], Decimal("50.00"))

    def test_edge_cases(self):
        """
        Test system robustness against common file-system and data errors.
        """
        # Case 1: Missing file - The system should treat a missing file as a fresh start, not an error.
        missing_handler = CSVHandler("missing.csv")
        tracker_missing = Tracker(missing_handler)
        tracker_missing.load_from_disk()
        self.assertEqual(len(tracker_missing.get_all_expenses()), 0)

        # Case 2: Empty file (only contains header) - Should load as 0 expenses.
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("amount,category,description,date\n")

        self.tracker.load_from_disk()
        self.assertEqual(len(self.tracker.get_all_expenses()), 0)

        # Case 3: File with invalid/negative numbers - The storage layer should
        # skip individual corrupted rows while still loading the valid ones.
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("amount,category,description,date\n")
            f.write("10.00,Food,Lunch,2023-01-01\n") # Valid
            f.write("-5.00,Food,Error,2023-01-02\n")   # Invalid (Negative)
            f.write("20.00,Transport,Taxi,2023-01-03\n") # Valid

        self.tracker.load_from_disk()
        # Only the 2 valid rows should be loaded.
        self.assertEqual(len(self.tracker.get_all_expenses()), 2)

if __name__ == "__main__":
    unittest.main()
