# Project Specification: Personal Expense Tracker

## Project Overview
A Python 3.11 command-line application to track personal expenses. The application focuses on data integrity, preventing invalid data (like negative amounts) from entering the system, and providing basic reporting grouped by category.

## Technical Stack
- **Language:** Python 3.11
- **Data Storage:** CSV (Comma Separated Values)
- **Key Libraries:** `dataclasses` (for modeling), `csv` (for storage), `datetime` (for dates), `decimal` (for financial precision).

---

## 1. Component Architecture

### A. Data Model (`Expense`)
The "Single Source of Truth." A structured object that ensures any expense in the system is valid.
- **Responsibilities:** Type enforcement and logical validation (e.g., amount > 0).

### B. Storage Manager (`CSVHandler`)
The interface between the Python application and the physical disk.
- **Responsibilities:** Converting Python objects to CSV rows and vice versa.

### C. Expense Tracker Logic (`Tracker`)
The business logic layer that manages the collection of expenses.
- **Responsibilities:** Adding expenses, calculating totals, and coordinating with the Storage Manager.

### D. User Interface (`CLI`)
The interaction layer that handles user input and output.
- **Responsibilities:** Displaying menus, capturing input, and handling "retry loops" for invalid data.

---

## 2. Validation Strategy
To prevent "bad data" from entering the system, validation happens at three levels:
1. **UI Level:** Prompt the user until the input is formatted correctly.
2. **Model Level:** The `Expense` object refuses to be created if the data is logically invalid (e.g., negative amount).
3. **Storage Level:** The loader verifies that the CSV file hasn't been corrupted or manually edited with invalid values.

---

## 3. Implementation Roadmap

### Phase 1: The Validated Data Model
*Goal: Establish a robust blueprint for what an "Expense" is.*

- **Task 1.1: Define the Expense Data Structure**
    - Create a `dataclass` with fields: `amount` (Decimal), `category` (str), `description` (str), and `date` (date).
- **Task 1.2: Implement Custom Validation Exceptions**
    - Create an `ExpenseValidationError` class to provide specific error messages for invalid data.
- **Task 1.3: Implement Model Validation Logic**
    - Use `__post_init__` to ensure `amount > 0` and that required fields are not empty.
- **Task 1.4: Create Date Normalization Utility**
    - A helper function to convert user-provided date strings (YYYY-MM-DD) into Python `date` objects.
- **Task 1.5: Model Verification Script**
    - A test suite that attempts to create valid and invalid expenses to verify the "gatekeeper" logic works.

### Phase 2: Robust Storage Layer
*Goal: Ensure data can be saved and loaded without corruption.*

- **Task 2.1: CSV Schema Definition**
    - Define the exact order of columns for the CSV file to ensure consistency.
- **Task 2.2: Implement `CSVHandler.save`**
    - Logic to write the current list of `Expense` objects to a CSV file.
- **Task 2.3: Implement `CSVHandler.load`**
    - Logic to read a CSV file and convert each row back into an `Expense` object.
- **Task 2.4: Implement Storage Ingestion Validation**
    - Ensure that the loader catches "dirty data" in the CSV (e.g., a string where the amount should be) and handles it gracefully.
- **Task 2.5: Storage Round-trip Test**
    - Verify that saving a list and then loading it back results in the exact same data.

### Phase 3: Core Tracker Logic
*Goal: Build the "brain" that manages the expense list and calculations.*

- **Task 3.1: Implement Tracker State Management**
    - Create a `Tracker` class that maintains an internal list of `Expense` objects.
- **Task 3.2: Implement Expense Addition**
    - Method to add a new validated `Expense` object to the internal list.
- **Task 3.3: Implement Expense Retrieval**
    - Method to return the full list of expenses for the UI to display.
- **Task 3.4: Implement Category Aggregation**
    - Logic to group expenses by category and sum their amounts (e.g., "Food: $120, Transport: $40").
- **Task 3.5: Implement Storage Bridge**
    - Connect the `Tracker` logic to the `CSVHandler` so the user can trigger save/load actions.

### Phase 4: Validating User Interface (CLI)
*Goal: Create a user-friendly way to interact with the system.*

- **Task 4.1: Implement Main Menu Loop**
    - A loop that displays options (Add, View All, View Totals, Save, Load, Exit) and captures the user's choice.
- **Task 4.2: Implement "Add Expense" Flow**
    - A series of prompts to collect amount, category, description, and date.
- **Task 4.3: Implement Input Validation Loops**
    - Wrap prompts in `while` loops that keep asking for a value until the `Date Normalization Utility` and `Expense` model accept it.
- **Task 4.4: Implement "View All" Display**
    - Format the list of expenses into a readable table.
- **Task 4.5: Implement "View Totals" Display**
    - Present the category-grouped totals in a clean report format.
- **Task 4.6: Implement Save/Load Commands**
    - Connect the menu options to the `Tracker`'s storage bridge.

### Phase 5: Final Testing & Polish
*Goal: Ensure the system is stable and handles edge cases.*

- **Task 5.1: End-to-End Integration Test**
    - A full run-through: Add expenses $\rightarrow$ Save $\rightarrow$ Restart $\rightarrow$ Load $\rightarrow$ View Totals.
- **Task 5.2: Edge Case Stress Test**
    - Attempt to load an empty CSV, a missing CSV, or a CSV with manually inserted negative numbers.
- **Task 5.3: UI Polish**
    - Add headers, clear separators, and helpful prompts to improve the user experience.
- **Task 5.4: Final Code Review & Documentation**
    - Ensure naming is consistent and the code follows Python 3.11 idioms.
