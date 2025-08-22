# Expense Tracker

A small, test-covered Python CLI app to track expenses and incomes by month. Data is stored in JSON and the UI uses `pystyle` when available (the app falls back to plain text when not).

## Features

- Record expenses and incomes grouped by month (YYYY-MM).
- View expenses by category and see totals.
- Add recurring monthly subscriptions and a fixed monthly salary that are applied automatically each month.
- Export a month's transactions to CSV; import transactions and subscriptions from CSV.
- Analytics for week, month, and year (expenses, income, profit, category breakdown).

- Lightweight fallback UI when `pystyle` is not installed so tests and CI runs cleanly.

## Quick start

Requirements

- Python 3.8+
- (Optional) `pystyle` to enable the colored/styled UI. The program runs without it.

Install dependencies (recommended in a virtualenv):

```powershell
pip install -r requirements.txt
```

Run the app:

```powershell
python project.py
```

Run tests:

```powershell
python -m pytest -q
```

## Data files

- `expenses.json` — main storage for expense transactions keyed by month.
- `incomes.json` — main storage for income transactions keyed by month.
- `user_data.json` — user profile information, subscriptions and fixed salary settings.

These files are created automatically on first run.

## CSV import/export

- Export a month's expenses to CSV (via code): `export_month_to_csv(month)` — writes `{month}_expenses.csv` by default.
- Import transactions from CSV: `import_csv(path)` expects a header with at least `date,category,amount` and an optional `kind` column. Valid `kind` values: `expense`, `income`, `subscription`, `salary`.

Example CSV rows:

```csv
date,category,amount,kind
2024-07-01,Gift,200,income
2024-07-02,Spotify,5,subscription
2024-07-02,Dinner,30,expense
```

When importing `subscription` rows, the subscription will be added to user subscriptions and applied for the month of the date.

## Subscriptions & Fixed Salary

- Add subscriptions programmatically or via the UI: these are monthly expenses that will be added automatically each new month.
- Fixed salary: a single monthly income that can be configured; it will be automatically added to incomes each month.

APIs (examples):

```python
from project import ExpenseTracker
tracker = ExpenseTracker('You')
tracker.add_subscription('Netflix', 9.99)
tracker.set_fixed_salary(1500.0)
tracker.apply_monthly_recurring('2025-08')
```

## Analytics

Use `analytics(period, reference)` where `period` is `week`, `month`, or `year`.

- For `month` use reference `YYYY-MM` (defaults to current month).
- For `year` use reference `YYYY` (defaults to current year).
- For `week` use reference `YYYY-MM-DD` representing any day in the week (defaults to today).

Returns: a dict with `expenses`, `income`, `profit`, `breakdown` by category and `period` label.

## Testing notes

- Tests are available in `test_project.py`. The suite covers import/export, subscriptions, salary, analytics, and core CRUD operations.
- Tests will create and remove JSON and CSV files during runs.

## Troubleshooting

- If colors/UI look wrong, install `pystyle` or continue without it. The app will still work.
- If the app doesn't record items, check the JSON files created in the project folder.

## Contributing

PRs are welcome. If you add features, please add or update unit tests in `test_project.py`.
