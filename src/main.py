"""
The entry point for the Personal Expense Tracker application.
This module handles the 'Composition Root'—initializing and wiring together
the various components (Storage, Tracker, and CLI) before starting the app.
"""

from src.storage import CSVHandler
from src.tracker import Tracker
from src.cli import CLI

def main():
    """
    Composition Root of the application.

    Educational Note: This function is responsible for wiring together the
    different components of the system. By initializing the storage handler,
    tracker, and CLI here, we can easily change a component's configuration
    (like the filename) without touching the logic inside the classes.
    """
    # 1. Initialize Storage: Decide where the data is stored on disk
    storage_handler = CSVHandler("expenses.csv")

    # 2. Initialize Tracker: The 'brain' that uses the storage handler
    tracker = Tracker(storage_handler)

    # 3. Automatically load existing data from disk on startup
    tracker.load_from_disk()

    # 4. Initialize CLI: The user interface that interacts with the tracker
    cli = CLI(tracker)

    # Start the application loop
    cli.run()

if __name__ == "__main__":
    main()
