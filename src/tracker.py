"""
This module implements the business logic of the Expense Tracker.
It manages the collection of expenses in memory and coordinates
with the storage handler to persist data to disk.
"""

from typing import List, Dict
from decimal import Decimal
from src.models import Expense
from src.storage import CSVHandler

class Tracker:
    """
    The core business logic layer that manages expenses and their persistence.

    Design Choice: The Tracker maintains an in-memory list of expenses for fast access.
    Persistence is delegated to a storage handler, separating 'what to do' from 'how to save'.
    """
    def __init__(self, storage_handler: CSVHandler):
        # Educational Note: Dependency Injection.
        # By passing CSVHandler into the constructor, Tracker doesn't need to know
        # how the files are actually saved. This makes it easy to swap CSV for a database later.
        self.storage = storage_handler
        self._expenses: List[Expense] = []

    def add_expense(self, expense: Expense):
        """
        Adds a validated Expense object to the internal state.
        """
        self._expenses.append(expense)

    def get_all_expenses(self) -> List[Expense]:
        """
        Returns the full list of tracked expenses.
        """
        return self._expenses

    def get_category_totals(self) -> Dict[str, Decimal]:
        """
        Groups expenses by category and calculates the total for each.

        Assumption: Category names are case-sensitive (e.g., 'Food' and 'food'
        are treated as different categories).
        """
        totals: Dict[str, Decimal] = {}
        for exp in self._expenses:
            # Using .get() with a default Decimal allows for a clean additive loop.
            totals[exp.category] = totals.get(exp.category, Decimal("0.00")) + exp.amount
        return totals

    def filter_by_category(self, category: str) -> List[Expense]:
        """
        Returns a list of expenses that match the given category.
        Search is case-insensitive.
        """
        return [exp for exp in self._expenses if exp.category.lower() == category.lower()]

    def get_unique_categories(self) -> List[str]:
        """
        Returns a sorted list of all unique categories currently in the system.
        """
        return sorted(list(set(exp.category for exp in self._expenses)))

    def save_to_disk(self):
        """
        Triggers the storage handler to save the current in-memory state to the main file.
        """
        self.storage.save(self._expenses)

    def load_from_disk(self):
        """
        Triggers the storage handler to read expenses from the main file and
        update the current in-memory state.
        """
        self._expenses = self.storage.load()
