"""
This module implements the Command Line Interface (CLI) for the application.
It handles all user interaction, including menu navigation, data input,
and the display of reported data.
"""

from decimal import Decimal, InvalidOperation
from src.models import Expense, ExpenseValidationError
from src.utils import parse_date
from src.tracker import Tracker
from src.storage import CSVHandler

class CLI:
    """
    User interaction layer for the Personal Expense Tracker.
    """
    def __init__(self, tracker: Tracker):
        self.tracker = tracker

    def run(self):
        """
        Main menu loop.
        """
        # Design Choice: Mapping keys to methods in a dictionary replaces
        # long if/elif chains, making the menu easily extensible.
        actions = {
            "1": self.add_expense_flow,
            "2": self.view_all_expenses,
            "3": self.view_category_totals,
            "4": self.filter_and_export_flow,
            "5": self.save_expenses,
            "6": self.load_expenses,
            "7": self.exit_app
        }

        while True:
            # Display the Main Menu
            print("\n" + "="*30)
            print("   PERSONAL EXPENSE TRACKER")
            print("="*30)
            print("1. Add Expense")
            print("2. View All Expenses")
            print("3. View Category Totals")
            print("4. Filter and Export by Category")
            print("5. Save to Disk")
            print("6. Load from Disk")
            print("7. Exit")
            print("="*30)

            choice = input("\nSelect an option: ").strip()

            # Execute the action associated with the user's choice
            if choice in actions:
                actions[choice]()
            else:
                print("Invalid choice, please try again.")

    def add_expense_flow(self):
        """
        Collects expense data with input validation.

        Educational Note: 'Input Validation Loop'.
        We wrap each prompt in a while-loop to prevent 'bad data' from ever reaching
        the model layer. This keeps the user in the prompt until the data is correct.
        """
        print("\n--- Add New Expense ---")

        # 1. Amount Validation Loop: Ensures input is a valid number
        while True:
            try:
                amount_str = input("Enter amount: ").strip()
                amount = Decimal(amount_str)
                break
            except InvalidOperation:
                print("Invalid input. Please enter a numeric value (e.g., 10.50).")

        # 2. Category Validation Loop: Ensures category is not empty
        while True:
            category = input("Enter category: ").strip()
            if category:
                break
            print("Category cannot be empty.")

        # 3. Description Validation Loop: Ensures description is not empty
        while True:
            description = input("Enter description: ").strip()
            if description:
                break
            print("Description cannot be empty.")

        # 4. Date Validation Loop: Ensures date follows YYYY-MM-DD format
        while True:
            date_str = input("Enter date (YYYY-MM-DD): ").strip()
            parsed_date = parse_date(date_str)
            if parsed_date:
                break
            print("Invalid date format. Please use YYYY-MM-DD.")

        try:
            # The final Expense object instantiation performs the last check
            # for logical consistency (e.g. amount > 0).
            expense = Expense(
                amount=amount,
                category=category,
                description=description,
                date=parsed_date
            )
            self.tracker.add_expense(expense)
            print("Expense added successfully!")
        except ExpenseValidationError as e:
            print(f"Failed to add expense: {e}")

    def view_all_expenses(self):
        """
        Displays all expenses in a table format.
        """
        expenses = self.tracker.get_all_expenses()
        if not expenses:
            print("\nNo expenses tracked yet.")
            return

        print("\n--- All Expenses ---")
        # Educational Note: f-string alignment.
        # ':<12' means left-aligned with 12 characters of padding.
        print(f"{'Date':<12} | {'Category':<15} | {'Amount':<10} | {'Description'}")
        print("-" * 60)
        for exp in expenses:
            print(f"{exp.date.isoformat():<12} | {exp.category:<15} | {exp.amount:<10.2f} | {exp.description}")

    def view_category_totals(self):
        """
        Displays totals grouped by category.
        """
        totals = self.tracker.get_category_totals()
        if not totals:
            print("\nNo expenses to calculate totals for.")
            return

        print("\n--- Category Totals ---")
        for category, total in totals.items():
            print(f"{category:<15}: ${total:>10.2f}")

    def filter_and_export_flow(self):
        """
        Flow to filter expenses by category and optionally export them to CSV.
        """
        print("\n--- Filter and Export ---")

        # 1. Retrieve and list available categories
        categories = self.tracker.get_unique_categories()
        if not categories:
            print("No categories available. Please add some expenses first.")
            return

        print("Available Categories:")
        for idx, cat in enumerate(categories, start=1):
            print(f"{idx}. {cat}")

        # 2. Handle user selection (allows either number or name)
        user_input = input("\nSelect category number or enter category name: ").strip()
        if not user_input:
            print("Input cannot be empty.")
            return

        try:
            choice_idx = int(user_input)
            if 1 <= choice_idx <= len(categories):
                category = categories[choice_idx - 1]
            else:
                print(f"Invalid selection. Please choose a number between 1 and {len(categories)}.")
                return
        except ValueError:
            category = user_input

        # 3. Filter the data
        filtered = self.tracker.filter_by_category(category)
        if not filtered:
            print(f"No expenses found for category: {category}")
            return

        # 4. Display the results in a table
        print(f"\n--- Results for Category: {category} ---")
        print(f"{'Date':<12} | {'Category':<15} | {'Amount':<10} | {'Description'}")
        print("-" * 60)
        for exp in filtered:
            print(f"{exp.date.isoformat():<12} | {exp.category:<15} | {exp.amount:<10.2f} | {exp.description}")

        # 5. Optional Export
        export_choice = input("\nWould you like to export these results to a CSV file? (y/n): ").strip().lower()
        if export_choice == 'y':
            filename = input("Enter filename for export (e.g., food_expenses.csv): ").strip()
            if not filename:
                print("Filename cannot be empty. Export cancelled.")
                return

            # Use the storage handler to save the subset of data
            self.tracker.storage.save_to_custom_file(filtered, filename)
            print(f"Successfully exported {len(filtered)} expenses to {filename}")
        else:
            print("Export cancelled.")

    def save_expenses(self):
        """Connects menu option to storage save."""
        self.tracker.save_to_disk()
        print("Expenses saved to disk successfully.")

    def load_expenses(self):
        """Connects menu option to storage load."""
        self.tracker.load_from_disk()
        print("Expenses loaded from disk successfully.")

    def exit_app(self):
        """
        Saves current state and exits the application.
        """
        print("\nSaving expenses...")
        self.tracker.save_to_disk()
        print("Exiting... Goodbye!")
        exit(0)
