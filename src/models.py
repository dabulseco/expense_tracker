"""
This module defines the core data structures for the Expense Tracker.
It ensures that every expense object created is logically valid before it
can be used by other parts of the application.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

class ExpenseValidationError(Exception):
    """Custom exception for errors during Expense object validation."""
    pass

@dataclass
class Expense:
    """
    Represents a single financial expense.

    Design Choice: Used a @dataclass for a concise representation of a data-holding
    object. It automatically provides __init__ and __repr__ methods.

    Assumption: Each expense must have a positive amount, a non-empty category,
    a non-empty description, and a valid date.
    """
    # Using Decimal instead of float for amount to avoid binary floating-point
    # precision errors common in financial calculations.
    amount: Decimal
    category: str
    description: str
    date: date

    def __post_init__(self):
        """
        Perform logical validation after the dataclass has initialized the fields.

        This is the 'Gatekeeper' pattern: ensuring that an Expense object
        cannot exist in an invalid state.
        """
        # 1. Validate Amount Type
        if not isinstance(self.amount, Decimal):
            # Assumption: We allow numeric-like types that can be converted to Decimal
            # to make the object more flexible during instantiation.
            try:
                self.amount = Decimal(str(self.amount))
            except Exception:
                raise ExpenseValidationError(f"Amount must be a valid number: {self.amount}")

        # 2. Validate Amount Value
        if self.amount <= 0:
            raise ExpenseValidationError(f"Amount must be positive: {self.amount}")

        # 3. Validate Category
        if not self.category or not self.category.strip():
            raise ExpenseValidationError("Category cannot be empty.")

        # 4. Validate Description
        if not self.description or not self.description.strip():
            raise ExpenseValidationError("Description cannot be empty.")

        # 5. Validate Date Type
        if not isinstance(self.date, date):
            raise ExpenseValidationError(f"Date must be a datetime.date object: {self.date}")
