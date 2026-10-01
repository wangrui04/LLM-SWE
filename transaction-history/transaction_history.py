from datetime import date, datetime
from typing import Mapping, Sequence


def _parse_date(value: object, field_name: str) -> date:
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


def filter_transactions(
    transactions: Sequence[Mapping[str, object]],
    start_date: date | str | None = None,
    end_date: date | str | None = None,
) -> list[Mapping[str, object]]:
    """Filter transactions by their inclusive `date` field."""
    if start_date is None and end_date is None:
        return list(transactions)

    start = _parse_date(start_date, "start_date") if start_date is not None else None
    end = _parse_date(end_date, "end_date") if end_date is not None else None
    if start is not None and end is not None and start > end:
        raise ValueError("start_date must be on or before end_date")

    filtered = []
    for transaction in transactions:
        transaction_date = _parse_date(transaction.get("date"), "transaction date")
        if start is not None and transaction_date < start:
            continue
        if end is not None and transaction_date > end:
            continue
        filtered.append(transaction)
    return filtered