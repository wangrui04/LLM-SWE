# Transaction History

Implementation for the Transaction_History project.

## Category Filtering

`src/transaction_history/transaction_history.py` provides a dependency-free transaction model and filtering API:

- `available_categories(transactions)` returns unique category options for a selector.
- `filter_transactions(transactions, category=...)` matches categories without regard to capitalization or punctuation.
- Omit `category` or pass `None` to clear the category filter.
- Pass `start_date` and `end_date` to compose date and category filters.

## Transaction Search

- `filter_transactions(transactions, search=...)` matches the search term against merchant, description, and category.
- Search ignores capitalization, leading/trailing spaces, and repeated spaces, and matches partial terms (for example, `coff` finds `Blue Bottle Coffee`).
- Pass `None`, `""`, or whitespace to clear the search and restore the filtered or full list.
- Combine `search` with `category`, `start_date`, and `end_date`; all filters must match.
- `format_transactions(results)` renders the list, or `NO_RESULTS_MESSAGE` when nothing matches.

Run the focused tests from this folder:

```powershell
$env:PYTHONPATH = "src"
py -m unittest discover -s src/tests -v
```
