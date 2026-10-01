import unittest
from datetime import date

from transaction_history import (
    NO_RESULTS_MESSAGE,
    Transaction,
    available_categories,
    filter_transactions,
    format_transactions,
)


class TransactionHistoryTests(unittest.TestCase):
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


class CategoryFilteringTests(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            Transaction(date(2026, 1, 2), "Coffee", 4.50, "Food & Dining"),
            Transaction(date(2026, 1, 5), "Bus pass", 25.00, "Transport"),
            Transaction(date(2026, 2, 1), "Groceries", 80.00, "food-dining"),
            Transaction(date(2026, 2, 4), "Salary", 2000.00, None),
        ]

    def test_available_categories_are_unique_and_displayable(self):
        self.assertEqual(
            available_categories(self.transactions),
            ["Food & Dining", "Transport"],
        )

    def test_category_filter_ignores_capitalization_and_formatting(self):
        results = filter_transactions(self.transactions, category=" food dining ")

        self.assertEqual([transaction.description for transaction in results], ["Coffee", "Groceries"])

    def test_other_categories_are_excluded(self):
        results = filter_transactions(self.transactions, category="Transport")

        self.assertEqual([transaction.description for transaction in results], ["Bus pass"])

    def test_clearing_category_restores_all_transactions(self):
        results = filter_transactions(self.transactions, category=None)

        self.assertEqual(results, self.transactions)

    def test_missing_category_is_excluded_when_category_is_selected(self):
        results = filter_transactions(self.transactions, category="Other")

        self.assertEqual(results, [])

    def test_no_matching_category_returns_empty_result(self):
        self.assertEqual(filter_transactions(self.transactions, category="Utilities"), [])

    def test_category_and_date_filters_are_applied_together(self):
        results = filter_transactions(
            self.transactions,
            category="FOOD DINING",
            start_date="2026-02-01",
            end_date="2026-02-28",
        )

        self.assertEqual([transaction.description for transaction in results], ["Groceries"])

    def test_invalid_date_range_is_rejected(self):
        with self.assertRaises(ValueError):
            filter_transactions(
                self.transactions,
                start_date="2026-03-01",
                end_date="2026-02-01",
            )


SEARCH_TRANSACTIONS = [
    Transaction(date(2026, 1, 2), "Morning latte", 4.50, "Food & Dining", "Blue Bottle Coffee"),
    Transaction(date(2026, 1, 9), "Weekly groceries", 62.10, "Food & Dining", "Trader Joe's"),
    Transaction(date(2026, 1, 15), "Monthly pass", 25.00, "Transport", "City Transit"),
    Transaction(date(2026, 2, 3), "Coffee beans", 18.00, "Food & Dining", "Blue Bottle Coffee"),
    Transaction(date(2026, 2, 10), "Refund", -12.00, None),
]


def descriptions(transactions):
    return [transaction.description for transaction in transactions]


class TransactionSearchTests(unittest.TestCase):
    def test_search_matches_merchant(self):
        results = filter_transactions(SEARCH_TRANSACTIONS, search="blue bottle")

        self.assertEqual(descriptions(results), ["Morning latte", "Coffee beans"])

    def test_search_matches_description(self):
        results = filter_transactions(SEARCH_TRANSACTIONS, search="groceries")

        self.assertEqual(descriptions(results), ["Weekly groceries"])

    def test_search_matches_category(self):
        results = filter_transactions(SEARCH_TRANSACTIONS, search="transport")

        self.assertEqual(descriptions(results), ["Monthly pass"])

    def test_search_matches_partial_terms(self):
        results = filter_transactions(SEARCH_TRANSACTIONS, search="coff")

        self.assertEqual(descriptions(results), ["Morning latte", "Coffee beans"])

    def test_search_is_case_insensitive(self):
        lower = filter_transactions(SEARCH_TRANSACTIONS, search="trader joe's")
        upper = filter_transactions(SEARCH_TRANSACTIONS, search="TRADER JOE'S")
        mixed = filter_transactions(SEARCH_TRANSACTIONS, search="TrAdEr JoE's")

        self.assertEqual(descriptions(lower), ["Weekly groceries"])
        self.assertEqual(upper, lower)
        self.assertEqual(mixed, lower)

    def test_leading_and_trailing_whitespace_is_ignored(self):
        results = filter_transactions(SEARCH_TRANSACTIONS, search="  refund\t ")

        self.assertEqual(descriptions(results), ["Refund"])

    def test_repeated_inner_whitespace_is_ignored(self):
        results = filter_transactions(SEARCH_TRANSACTIONS, search="city    transit")

        self.assertEqual(descriptions(results), ["Monthly pass"])

    def test_empty_search_returns_all_transactions(self):
        for search in (None, "", "   "):
            with self.subTest(search=search):
                self.assertEqual(filter_transactions(SEARCH_TRANSACTIONS, search=search), SEARCH_TRANSACTIONS)

    def test_no_match_returns_empty_result(self):
        self.assertEqual(filter_transactions(SEARCH_TRANSACTIONS, search="airline"), [])

    def test_no_match_displays_empty_state(self):
        results = filter_transactions(SEARCH_TRANSACTIONS, search="airline")

        self.assertEqual(format_transactions(results), NO_RESULTS_MESSAGE)

    def test_matches_are_displayed(self):
        results = filter_transactions(SEARCH_TRANSACTIONS, search="transit")

        self.assertEqual(format_transactions(results), "2026-01-15  City Transit  25.00")

    def test_clearing_search_restores_full_list(self):
        searched = filter_transactions(SEARCH_TRANSACTIONS, search="coffee")
        cleared = filter_transactions(SEARCH_TRANSACTIONS, search="")

        self.assertNotEqual(searched, SEARCH_TRANSACTIONS)
        self.assertEqual(cleared, SEARCH_TRANSACTIONS)

    def test_clearing_search_restores_filtered_list(self):
        filters = {"category": "Food & Dining", "start_date": "2026-01-01", "end_date": "2026-01-31"}
        cleared = filter_transactions(SEARCH_TRANSACTIONS, search=None, **filters)

        self.assertEqual(cleared, filter_transactions(SEARCH_TRANSACTIONS, **filters))
        self.assertEqual(descriptions(cleared), ["Morning latte", "Weekly groceries"])

    def test_search_with_date_filter(self):
        results = filter_transactions(
            SEARCH_TRANSACTIONS,
            search="blue bottle",
            start_date="2026-02-01",
            end_date="2026-02-28",
        )

        self.assertEqual(descriptions(results), ["Coffee beans"])

    def test_search_with_category_filter(self):
        results = filter_transactions(SEARCH_TRANSACTIONS, search="pass", category="food dining")

        self.assertEqual(results, [])

    def test_search_with_date_and_category_filters(self):
        results = filter_transactions(
            SEARCH_TRANSACTIONS,
            search=" COFFEE ",
            category="Food & Dining",
            start_date="2026-01-01",
            end_date="2026-01-31",
        )

        self.assertEqual(descriptions(results), ["Morning latte"])

    def test_non_string_search_is_rejected(self):
        with self.assertRaises(TypeError):
            filter_transactions(SEARCH_TRANSACTIONS, search=42)


if __name__ == "__main__":
    unittest.main()