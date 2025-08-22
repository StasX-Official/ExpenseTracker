import pytest
from project import load_data, add_expense, calculate_expenses, print_banner, ExpenseTracker
import os
import json

def test_load_data():
    assert load_data("nonexistent.json") == {}
    test_data = {"test": "data"}
    with open("test.json", "w") as f:
        json.dump(test_data, f)
    assert load_data("test.json") == test_data
    os.remove("test.json")

def test_add_expense():
    expenses = {}
    month = "2024-01"
    expenses = add_expense(expenses, "Food", 100, month)
    assert len(expenses[month]) == 1
    assert expenses[month][0]['amount'] == 100
    assert expenses[month][0]['category'] == "Food"
    expenses = add_expense(expenses, "Transport", 50, month)
    assert len(expenses[month]) == 2

def test_calculate_expenses():
    expenses = {
        "2024-01": [
            {"amount": 100, "category": "Food"},
            {"amount": 200, "category": "Transport"},
            {"amount": 150, "category": "Food"}
        ]
    }
    assert calculate_expenses(expenses, "2024-01") == 450
    assert calculate_expenses(expenses, "2024-01", "Food") == 250
    assert calculate_expenses(expenses, "2024-02") == 0

def test_print_banner(capsys):
    print_banner()
    captured = capsys.readouterr()
    assert captured.out

def test_expense_tracker_init():
    tracker = ExpenseTracker("TestUser")
    assert tracker.user_name == "TestUser"
    assert isinstance(tracker.expenses, dict)
    assert isinstance(tracker.user_data, dict)

def test_expense_tracker_add_expense():
    tracker = ExpenseTracker("TestUser")
    tracker.add_expense("Food", 50.0, "2024-01")
    assert "2024-01" in tracker.expenses
    assert len(tracker.expenses["2024-01"]) == 1
    assert tracker.expenses["2024-01"][0]["amount"] == 50.0
    assert tracker.expenses["2024-01"][0]["category"] == "Food"

def test_expense_tracker_remove_expense():
    tracker = ExpenseTracker("TestUser")
    tracker.add_expense("Food", 50.0, "2024-01")
    tracker.add_expense("Transport", 30.0, "2024-01")
    initial_length = len(tracker.expenses["2024-01"])
    tracker.remove_expense("2024-01", 0)
    assert len(tracker.expenses["2024-01"]) == initial_length - 1

def test_expense_tracker_view_expenses_by_category():
    tracker = ExpenseTracker("TestUser")
    tracker.add_expense("Food", 50.0, "2024-01")
    tracker.add_expense("Food", 30.0, "2024-01")
    tracker.add_expense("Transport", 20.0, "2024-01")
    
    expenses, total = tracker.view_expenses_by_category("2024-01", "Food")
    assert len(expenses) == 2
    assert total == 80.0

def test_expense_tracker_get_total_expenses():
    tracker = ExpenseTracker("TestUser")
    tracker.add_expense("Food", 50.0, "2024-01")
    tracker.add_expense("Transport", 30.0, "2024-01")
    
    total = tracker.get_total_expenses("2024-01")
    assert total == 80.0
    assert tracker.get_total_expenses("2024-02") == 0

def test_expense_tracker_file_operations():
    tracker = ExpenseTracker("TestUser")
    tracker.add_expense("Food", 50.0, "2024-01")
    assert os.path.exists(tracker.expenses_file)
    assert os.path.exists(tracker.user_data_path)
    os.remove(tracker.expenses_file)
    os.remove(tracker.user_data_path)

@pytest.fixture(autouse=True)
def cleanup():
    import glob
    files_to_cleanup = ['expenses.json', 'user_data.json', 'test.json', 'incomes.json', 'test_import.csv']
    files_to_cleanup += glob.glob('*_expenses.csv')
    yield
    for file in files_to_cleanup:
        if os.path.exists(file):
            os.remove(file)


def test_add_income_and_total():
    tracker = ExpenseTracker("TestUser")
    tracker.add_income("Job", 1000.0, "2024-01")
    assert "2024-01" in tracker.incomes
    assert len(tracker.incomes["2024-01"]) == 1
    assert tracker.get_total_income("2024-01") == 1000.0


def test_subscriptions_and_fixed_salary_application():
    tracker = ExpenseTracker("SubUser")
    tracker.user_data.pop('subscriptions', None)
    tracker.user_data.pop('fixed_salary', None)
    tracker.save_user_data()

    tracker.add_subscription("Netflix", 9.99)
    tracker.set_fixed_salary(1500.0)

    tracker.apply_monthly_recurring("2024-05")

    assert any(e.get('category') == 'Netflix' and float(e.get('amount')) == 9.99 for e in tracker.expenses.get('2024-05', []))
    assert any(i.get('category') == 'Salary' and float(i.get('amount')) == 1500.0 for i in tracker.incomes.get('2024-05', []))


def test_export_and_import_csv():
    tracker = ExpenseTracker("CSVUser")
    tracker.expenses['2024-06'] = [{'category': 'Food', 'amount': 50, 'date': '2024-06-10'}]
    tracker.incomes['2024-06'] = [{'category': 'Salary', 'amount': 1000, 'date': '2024-06-01'}]
    tracker.save_expenses()
    tracker.save_incomes()

    path = tracker.export_month_to_csv('2024-06')
    assert path is not None and os.path.exists(path)

    import_csv_path = 'test_import.csv'
    with open(import_csv_path, 'w', encoding='utf-8') as f:
        f.write('date,category,amount,kind\n')
        f.write('2024-07-01,Gift,200,income\n')
        f.write('2024-07-02,Spotify,5,subscription\n')
        f.write('2024-07-02,Dinner,30,expense\n')

    tracker.import_csv(import_csv_path)

    assert any(i.get('category') == 'Gift' and float(i.get('amount')) == 200 for i in tracker.incomes.get('2024-07', []))
    assert any(e.get('category') == 'Spotify' and float(e.get('amount')) == 5 for e in tracker.expenses.get('2024-07', []))
    assert any(s.get('category') == 'Spotify' for s in tracker.user_data.get('subscriptions', []))


def test_analytics_month_year_week_and_list_months():
    tracker = ExpenseTracker("Analyst")
    tracker.expenses = {
        '2024-08': [
            {'category': 'Food', 'amount': 100, 'date': '2024-08-10'},
            {'category': 'Transport', 'amount': 50, 'date': '2024-08-11'}
        ],
        '2024-07': [
            {'category': 'Misc', 'amount': 20, 'date': '2024-07-15'}
        ]
    }
    tracker.incomes = {
        '2024-08': [
            {'category': 'Salary', 'amount': 500, 'date': '2024-08-01'}
        ],
        '2024-07': [
            {'category': 'Gift', 'amount': 100, 'date': '2024-07-02'}
        ]
    }

    res_month = tracker.analytics(period='month', reference='2024-08')
    assert res_month['expenses'] == 150
    assert res_month['income'] == 500
    assert res_month['profit'] == 350

    res_year = tracker.analytics(period='year', reference='2024')
    assert res_year['expenses'] == 170
    assert res_year['income'] == 600

    res_week = tracker.analytics(period='week', reference='2024-08-10')
    assert res_week['expenses'] == 150

    months = tracker.list_months()
    assert '2024-07' in months and '2024-08' in months
