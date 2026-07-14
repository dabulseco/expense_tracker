"""
Unit tests for the Expense model and date utility functions.
This suite verifies the 'Gatekeeper' logic: ensuring that invalid data
cannot be used to create an Expense object.
"""

import unittest
from decimal import Decimal
from datetime import date
from src.models import Expense, ExpenseValidationError
from src.utils import parse_date

class TestExpenseModel(unittest.TestCase):
    def test_valid_expense(self):
        """Verify that a valid Expense object can be created."""
        exp = Expense(
            amount=Decimal("10.50"),
            category="Food",
            description="Lunch",
            date=date(2023, 1, 1)
        )
        self.assertEqual(exp.amount, Decimal("10.50"))
        self.assertEqual(exp.category, "Food")

    def test_negative_amount(self):
        """Verify that negative amounts raise ExpenseValidationError."""
        with self.assertRaises(ExpenseValidationError) as cm:
            Expense(amount=Decimal("-10.00"), category="Food", description="Lunch", date=date.today())
        self.assertIn("Amount must be positive", str(cm.exception))

    def test_zero_amount(self):
        """Verify that zero amounts raise ExpenseValidationError."""
        with self.assertRaises(ExpenseValidationError) as cm:
            Expense(amount=Decimal("0.00"), category="Food", description="Lunch", date=date.today())
        self.assertIn("Amount must be positive", str(cm.exception))

    def test_empty_category(self):
        """Verify that empty categories raise ExpenseValidationError."""
        with self.assertRaises(ExpenseValidationError) as cm:
            Expense(amount=Decimal("10.00"), category="", description="Lunch", date=date.today())
        self.assertIn("Category cannot be empty", str(cm.exception))

    def test_empty_description(self):
        """Verify that empty descriptions raise ExpenseValidationError."""
        with self.assertRaises(ExpenseValidationError) as cm:
            Expense(amount=Decimal("10.00"), category="Food", description="  ", date=date.today())
        self.assertIn("Description cannot be empty", str(cm.exception))

    def test_invalid_date_type(self):
        """Verify that non-date objects raise ExpenseValidationError."""
        with self.assertRaises(ExpenseValidationError) as cm:
            Expense(amount=Decimal("10.00"), category="Food", description="Lunch", date="2023-01-01")
        self.assertIn("Date must be a datetime.date object", str(cm.exception))

class TestUtils(unittest.TestCase):
    def test_parse_date_valid(self):
        """Verify that valid YYYY-MM-DD strings are parsed correctly."""
        self.assertEqual(parse_date("2023-12-25"), date(2023, 12, 25))

    def test_parse_date_invalid(self):
        """Verify that invalid date strings return None."""
        # Test incorrect separator
        self.assertIsNone(parse_date("2023/12/25"))
        # Test non-numeric input
        self.assertIsNone(parse_date("invalid-date"))
        # Test logically invalid date (month 13)
        self.assertIsNone(parse_date("2023-13-01"))

if __name__ == "__main__":
    unittest.main()
