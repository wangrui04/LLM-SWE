"""Transaction models and filtering utilities."""

from dataclasses import dataclass
from datetime import date, datetime
import re
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class Transaction:
    """A transaction record that can be filtered by date and category."""

    date: date
    description: str
    amount: float
    category: str | None = None


def _parse_date_value(value: object, field_name: str) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError as error:
            raise ValueError(f"{field_name} must be a valid ISO date") from error
    raise ValueError(f"{field_name} must be a date or ISO date string")


def normalize_category(category: str | None) -> str | None:
    """Return a case- and formatting-insensitive category key."""
    if category is None:
        return None

    normalized = re.sub(r"[^a-z0-9]+", " ", category.casefold()).strip()
    return normalized or None


def available_categories(transactions: Iterable[Transaction]) -> list[str]:
    """Return unique, display-ready category options in alphabetical order."""
    categories: dict[str, str] = {}
    for transaction in transactions:
        key = normalize_category(transaction.category)
        if key is not None and key not in categories:
            categories[key] = transaction.category.strip()

    return [categories[key] for key in sorted(categories)]


def _filter_mapping_transactions(
    transactions: Sequence[Mapping[str, object]],
    start_date: date | str | None,
    end_date: date | str | None,
) -> list[Mapping[str, object]]:
    if start_date is None and end_date is None:
        return list(transactions)

    start = _parse_date_value(start_date, "start_date") if start_date is not None else None
    end = _parse_date_value(end_date, "end_date") if end_date is not None else None
    if start is not None and end is not None and start > end:
        raise ValueError("start_date must be on or before end_date")

    filtered = []
    for transaction in transactions:
        transaction_date = _parse_date_value(transaction.get("date"), "transaction date")
        if start is not None and transaction_date < start:
            continue
        if end is not None and transaction_date > end:
            continue
        filtered.append(transaction)
    return filtered


def _filter_transaction_records(
    transactions: Iterable[Transaction],
    category: str | None,
    start_date: date | str | None,
    end_date: date | str | None,
) -> list[Transaction]:
    start = _parse_date_value(start_date, "start_date") if start_date is not None else None
    end = _parse_date_value(end_date, "end_date") if end_date is not None else None
    if start is not None and end is not None and start > end:
        raise ValueError("start_date must be on or before end_date")

    category_key = normalize_category(category)
    return [
        transaction
        for transaction in transactions
        if (category_key is None or normalize_category(transaction.category) == category_key)
        and (start is None or transaction.date >= start)
        and (end is None or transaction.date <= end)
    ]


def filter_transactions(
    transactions: Iterable[Transaction] | Sequence[Mapping[str, object]],
    start_date: date | str | None = None,
    end_date: date | str | None = None,
    *,
    category: str | None = None,
) -> list[Transaction] | list[Mapping[str, object]]:
    """Filter mapping records by date or Transaction records by date and category."""
    items = list(transactions)
    if items and isinstance(items[0], Mapping):
        if category is not None:
            raise ValueError("category filtering requires Transaction records")
        return _filter_mapping_transactions(items, start_date, end_date)

    return _filter_transaction_records(items, category, start_date, end_date)