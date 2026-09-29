"""Filtering utilities for transaction history records."""

from dataclasses import dataclass
from datetime import date
import re
from typing import Iterable


@dataclass(frozen=True)
class Transaction:
    """A transaction record that can be filtered by date, category, and search."""

    date: date
    description: str
    amount: float
    category: str | None = None
    merchant: str | None = None


NO_RESULTS_MESSAGE = "No transactions match your search."


def normalize_category(category: str | None) -> str | None:
    """Return a case- and formatting-insensitive category key."""
    if category is None:
        return None

    normalized = re.sub(r"[^a-z0-9]+", " ", category.casefold()).strip()
    return normalized or None


def normalize_search(search: str | None) -> str | None:
    """Return a case-insensitive search key with surrounding and repeated spaces removed.

    An empty or whitespace-only search clears the search filter.
    """
    if search is None:
        return None
    if not isinstance(search, str):
        raise TypeError("search must be a string or None")

    normalized = " ".join(search.casefold().split())
    return normalized or None


def _matches_search(transaction: Transaction, search_key: str) -> bool:
    fields = (transaction.merchant, transaction.description, transaction.category)
    return any(
        field is not None and search_key in " ".join(field.casefold().split())
        for field in fields
    )


def available_categories(transactions: Iterable[Transaction]) -> list[str]:
    """Return unique, display-ready category options in alphabetical order."""
    categories: dict[str, str] = {}
    for transaction in transactions:
        key = normalize_category(transaction.category)
        if key is not None and key not in categories:
            categories[key] = transaction.category.strip()

    return [categories[key] for key in sorted(categories)]


def _parse_date(value: date | str | None) -> date | None:
    if value is None or isinstance(value, date):
        return value
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"Invalid date: {value!r}; use YYYY-MM-DD") from error


def filter_transactions(
    transactions: Iterable[Transaction],
    *,
    category: str | None = None,
    start_date: date | str | None = None,
    end_date: date | str | None = None,
    search: str | None = None,
) -> list[Transaction]:
    """Filter transactions by category, inclusive date bounds, and a search term.

    A missing category or an empty category selection clears the category filter.
    Category matching ignores capitalization, whitespace, and punctuation.
    Search matches merchant, description, or category, ignoring capitalization
    and extra whitespace; an empty search clears the search filter.
    """
    start = _parse_date(start_date)
    end = _parse_date(end_date)
    if start is not None and end is not None and start > end:
        raise ValueError("start_date must be before or equal to end_date")

    category_key = normalize_category(category)
    search_key = normalize_search(search)
    return [
        transaction
        for transaction in transactions
        if (category_key is None or normalize_category(transaction.category) == category_key)
        and (start is None or transaction.date >= start)
        and (end is None or transaction.date <= end)
        and (search_key is None or _matches_search(transaction, search_key))
    ]


def format_transactions(transactions: Iterable[Transaction]) -> str:
    """Render transactions one per line, or an empty-state message when there are none."""
    lines = [
        f"{transaction.date.isoformat()}  {transaction.merchant or transaction.description}"
        f"  {transaction.amount:.2f}"
        for transaction in transactions
    ]
    return "\n".join(lines) if lines else NO_RESULTS_MESSAGE
