import unittest
from datetime import date

from transaction_history import filter_transactions


class FilterTransactionsTests(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            {"date": "2025-01-01", "description": "Before"},
            {"date": "2025-01-02", "description": "Start boundary"},
            {"date": "2025-01-03", "description": "Inside"},
            {"date": "2025-01-04", "description": "End boundary"},
            {"date": "2025-01-05", "description": "After"},
        ]

    def test_filters_inclusive_date_range(self):
        result = filter_transactions(self.transactions, "2025-01-02", "2025-01-04")

        self.assertEqual(
            [item["description"] for item in result],
            ["Start boundary", "Inside", "End boundary"],
        )

    def test_accepts_one_sided_bounds_and_date_objects(self):
        after_start = filter_transactions(self.transactions, date(2025, 1, 4))
        before_end = filter_transactions(self.transactions, end_date="2025-01-02")

        self.assertEqual(len(after_start), 2)
        self.assertEqual(len(before_end), 2)

    def test_same_start_and_end_date_is_inclusive(self):
        result = filter_transactions(self.transactions, "2025-01-03", "2025-01-03")

        self.assertEqual([item["description"] for item in result], ["Inside"])

    def test_clearing_bounds_returns_all_transactions(self):
        self.assertEqual(filter_transactions(self.transactions), self.transactions)

    def test_empty_matching_range_returns_no_transactions(self):
        result = filter_transactions(self.transactions, "2025-02-01", "2025-02-10")

        self.assertEqual(result, [])

    def test_reversed_range_is_rejected(self):
        with self.assertRaises(ValueError):
            filter_transactions(self.transactions, "2025-01-04", "2025-01-02")

    def test_invalid_date_is_rejected(self):
        with self.assertRaises(ValueError):
            filter_transactions(self.transactions, "not-a-date")


if __name__ == "__main__":
    unittest.main()