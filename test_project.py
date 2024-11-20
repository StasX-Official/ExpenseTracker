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
    files_to_cleanup = ['expenses.json', 'user_data.json', 'test.json']
    yield
    for file in files_to_cleanup:
        if os.path.exists(file):
            os.remove(file)
