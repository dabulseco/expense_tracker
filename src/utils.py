"""
This module provides shared utility functions used across the application.
Its primary goal is to centralize common logic, such as date parsing and
normalization, to ensure consistency across the UI and Storage layers.
"""

from datetime import datetime, date
from typing import Optional

def parse_date(date_str: str) -> Optional[date]:
    """
    Converts a date string in YYYY-MM-DD format to a datetime.date object.
    Returns None if the format is invalid.

    Assumption: We use the ISO 8601 format (YYYY-MM-DD) because it is the
    international standard, avoids ambiguity between US/UK date formats,
    and sorts naturally as a string.

    Assumption: The application only tracks dates, not times or timezones,
    which simplifies the logic for a personal expense tracker.
    """
    try:
        # Attempt to parse the string. If it doesn't match %Y-%m-%d,
        # a ValueError is raised.
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        # Return None so the caller (e.g., the CLI) can handle the error
        # and prompt the user to try again.
        return None
