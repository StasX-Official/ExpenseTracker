from pystyle import Colors, Colorate, Center, Write, Box, Anime, System
import os
import sys
import json
from datetime import datetime
import time

def print_banner():
    banner = """  _____                                  _____               _
 | ____|_  ___ __   ___ _ __  ___  ___  |_   _| __ __ _  ___| | _____ _ __
 |  _| \ \/ / '_ \ / _ \ '_ \/ __|/ _ \   | || '__/ _` |/ __| |/ / _ \ '__|
 | |___ >  <| |_) |  __/ | | \__ \  __/   | || | | (_| | (__|   <  __/ |
 |_____/_/\_\ .__/ \___|_| |_|___/\___|   |_||_|  \__,_|\___|_|\_\___|_|
            |_|                                                           """
    print(Colorate.Diagonal(Colors.blue_to_purple, banner))
    time.sleep(1)

def show_menu_header():
    pass

def show_menu_options():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    menu = """
    
    [1] 📊   Analysis      
    [2] 💰   Add Expense   
    [3] 🗑️   Remove       
    [4]  ℹ️  Info         
    [5] 🚪   Exit 
    """
    print(Colorate.Horizontal(Colors.blue_to_purple, menu))

def show_loading_animation():
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for i in range(20):
        print(f"\rLoading {chars[i % len(chars)]}", end="")
        time.sleep(0.1)
    print()

def load_data(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        return {}
    except Exception as e:
        Write.Print(f"\n Error loading data: {e}", Colors.red_to_yellow, interval=0.05)
        return {}

def add_expense(expenses, category, amount, month):
    try:
        expense = {
            'category': category,
            'amount': float(amount),
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        if month not in expenses:
            expenses[month] = []
        expenses[month].append(expense)
        return expenses
    except Exception:
        return expenses

def calculate_expenses(expenses, month, category=None):
    try:
        if month not in expenses:
            return 0
        if category:
            return sum(exp['amount'] for exp in expenses[month] 
                      if exp['category'] == category)
        return sum(exp['amount'] for exp in expenses[month])
    except Exception:
        return 0

class ExpenseTracker:
    def __init__(self, user_name):
        self.user_name = user_name
        self.user_data_path = 'user_data.json'
        self.expenses_file = 'expenses.json'
        show_loading_animation()
        self.user_data = self.load_user_data()
        self.expenses = self.load_expenses()
        self.banner = print_banner

    def load_user_data(self):
        try:
            if os.path.exists(self.user_data_path):
                with open(self.user_data_path, 'r') as file:
                    return json.load(file)
            else:
                return {}
        except Exception as e:
            Write.Print(f"\n Error loading user data: {e}", Colors.red_to_yellow, interval=0.05)
            return {}

    def save_user_data(self):
        try:
            with open(self.user_data_path, 'w') as file:
                json.dump(self.user_data, file, indent=4)
        except Exception as e:
            Write.Print(f"\n Error saving user data: {e}", Colors.red_to_yellow, interval=0.05)

    def load_expenses(self):
        try:
            if os.path.exists(self.expenses_file):
                with open(self.expenses_file, 'r') as file:
                    return json.load(file)
            else:
                return {}
        except Exception as e:
            Write.Print(f"\n Error loading expenses: {e}", Colors.red_to_yellow, interval=0.05)
            return {}

    def save_expenses(self):
        try:
            with open(self.expenses_file, 'w') as file:
                json.dump(self.expenses, file, indent=4)
        except Exception as e:
            Write.Print(f"\n Error saving expenses: {e}", Colors.red_to_yellow, interval=0.05)

    def add_expense(self, category, amount, month):
        try:
            expense = {
                'category': category,
                'amount': amount,
                'date': datetime.now().strftime("%Y-%m-%d")
            }
            if month not in self.expenses:
                self.expenses[month] = []
            self.expenses[month].append(expense)
            self.save_expenses()
            Write.Print("\n Expense added successfully!", Colors.green_to_blue, interval=0.05)
        except Exception as e:
            Write.Print(f"\n Error adding expense: {e}", Colors.red_to_yellow, interval=0.05)

    def remove_expense(self, month, index):
        try:
            if month in self.expenses and 0 <= index < len(self.expenses[month]):
                deleted_expense = self.expenses[month].pop(index)
                self.save_expenses()
                Write.Print(f"\n Expense removed: {deleted_expense}", Colors.red_to_yellow, interval=0.05)
            else:
                Write.Print("\n Invalid expense or month.", Colors.red_to_yellow, interval=0.05)
        except Exception as e:
            Write.Print(f"\n Error removing expense: {e}", Colors.red_to_yellow, interval=0.05)

    def view_expenses_by_category(self, month, category):
        try:
            if month in self.expenses:
                filtered_expenses = [expense for expense in self.expenses[month] if expense['category'] == category]
                total = sum(expense['amount'] for expense in filtered_expenses)
                return filtered_expenses, total
            else:
                Write.Print(f"\n No expenses found for {month}", Colors.red_to_yellow, interval=0.05)
                return [], 0
        except Exception as e:
            Write.Print(f"\n Error viewing expenses by category: {e}", Colors.red_to_yellow, interval=0.05)
            return [], 0

    def get_total_expenses(self, month):
        try:
            if month in self.expenses:
                total = sum(expense['amount'] for expense in self.expenses[month])
                return total
            else:
                Write.Print(f"\n No expenses found for {month}", Colors.red_to_yellow, interval=0.05)
                return 0
        except Exception as e:
            Write.Print(f"\n Error getting total expenses: {e}", Colors.red_to_yellow, interval=0.05)
            return 0

    def create_profile(self):
        try:
            Write.Print("\n Creating a new profile...", Colors.blue_to_purple, interval=0.05)
            self.user_name = Write.Input(" Enter your name > ", Colors.blue_to_purple, interval=0.05)
            self.user_data[self.user_name] = {
                'user_name': self.user_name
            }
            self.save_user_data()
        except Exception as e:
            Write.Print(f"\n Error creating profile: {e}", Colors.red_to_yellow, interval=0.05)

    def menu(self):
        try:
            System.Clear()
            self.banner()
            show_menu_header()

            if not self.user_data:
                self.create_profile()
            
            Write.Print(f"\n 👤 Welcome, {self.user_name}!", Colors.blue_to_purple, interval=0.05)
            Write.Print("\n 📱 Your personal expense tracker:", Colors.blue_to_purple, interval=0.05)
            
            while True:
                show_menu_options()
                choice = Write.Input("\n 🎯 Choose an option > ", Colors.blue_to_purple, interval=0.05)

                if choice == '1':
                    self.analyze_expenses()
                elif choice == '2':
                    self.record_expenses()
                elif choice == '3':
                    self.remove_expense_menu()
                elif choice == '4':
                    self.information()
                elif choice == '5':
                    Write.Print("\n Thanks for using Expense Tracker!", Colors.blue_to_purple, interval=0.05)
                    sys.exit()
                else:
                    Write.Print("\n Invalid option, please try again.", Colors.red_to_yellow, interval=0.05)

        except Exception as e:
            Write.Print(f"\n Error in menu: {e}", Colors.red_to_yellow, interval=0.05)

    def information(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.banner()
            info = """
 PROJECT INFORMATION
 Welcome to Expense Tracker!
 This app has been designed to help users effectively track and manage their expenses.
 From recording transactions to analyzing financial data, everything you need is just a few clicks away.

 The app allows you to:
 - Log expenses by category, keeping track of details and amounts.
 - View expenses organized by months and categories.
 - Remove expenses as needed.
 - Utilize a personal dashboard to maintain your financial history.

 The project was developed using Python, with data stored in JSON format, and the pystyle
 library to enhance the user interface.

 Enjoy using the app, and remember to regularly check your expenses!
"""
            print(Colorate.Horizontal(Colors.blue_to_purple, info))
            input("\nPress Enter...")
        except Exception as e:
            Write.Print(f"\n❌ Error: {e}", Colors.red_to_yellow)

    def show_section_header(self, title):
        header = f"""
╭───────────────────────╮
│     {title:<15} │
╰───────────────────────╯"""
        print(Colorate.Horizontal(Colors.blue_to_purple, header))

    def analyze_expenses(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.banner()
            self.show_section_header("ANALYSIS")
            
            month = Write.Input("\n📅 Enter month (YYYY-MM) > ", Colors.blue_to_purple, interval=0.02)
            
            if month in self.expenses:
                total = self.get_total_expenses(month)
                report = f"""
📊 Summary for {month}:
━━━━━━━━━━━━━━━━━
💰 Total: ${total}
🗓️  Items: {len(self.expenses[month])}"""
                print(Box.Lines(report))
                
                categories = set(exp['category'] for exp in self.expenses[month])
                for category in categories:
                    expenses, cat_total = self.view_expenses_by_category(month, category)
                    percentage = (cat_total / total) * 100 if total > 0 else 0
                    
                    cat_info = f"📌 {category}: ${cat_total} ({percentage:.1f}%)"
                    Write.Print(f"\n{cat_info}", Colors.blue_to_purple, interval=0.02)
                    
                    for exp in expenses:
                        exp_info = f"  └─❯ {exp['date']}: ${exp['amount']}"
                        Write.Print(f"\n{exp_info}", Colors.blue_to_cyan, interval=0.01)
                
                Write.Input("\n\n🔄 Press Enter to continue...", Colors.blue_to_purple, interval=0.02)
                
            else:
                Write.Print(f"\n❌ No expenses found for {month}", Colors.red_to_yellow, interval=0.02)
                
        except Exception as e:
            Write.Print(f"\n❌ Error: {e}", Colors.red_to_yellow, interval=0.02)

    def record_expenses(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.banner()
            self.show_section_header("NEW EXPENSE")
            
            category = Write.Input("\n 📁 Enter category > ", Colors.blue_to_purple, interval=0.05)
            amount = float(Write.Input(" 💵 Enter amount > ", Colors.blue_to_purple, interval=0.05))
            month = Write.Input(" 📅 Enter month (YYYY-MM) > ", Colors.blue_to_purple, interval=0.05)
            
            self.add_expense(category, amount, month)
            Write.Print("\n ✅ Expense added successfully!", Colors.green_to_blue, interval=0.05)
            Anime.Move(text="Processing...", color=Colors.blue_to_purple, time=1)
            
        except ValueError:
            Write.Print("\n ❌ Invalid amount! Please enter a number.", Colors.red_to_yellow, interval=0.05)
        except Exception as e:
            Write.Print(f"\n ❌ Error: {e}", Colors.red_to_yellow, interval=0.05)

    def remove_expense_menu(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.banner()
            self.show_section_header("REMOVE")
            month = Write.Input("\n Enter the month (YYYY-MM) of the expense to remove > ", Colors.blue_to_purple, interval=0.05)
            if month in self.expenses and self.expenses[month]:
                Write.Print(f"\n Expenses for {month}:", Colors.yellow_to_red, interval=0.05)
                for idx, expense in enumerate(self.expenses[month]):
                    Write.Print(f"{idx + 1}. {expense['date']}: {expense['amount']} ({expense['category']})", Colors.yellow_to_red, interval=0.02)
                index = int(Write.Input(f"\n Enter the number of the expense to remove (1-{len(self.expenses[month])}) > ", Colors.blue_to_purple, interval=0.05)) - 1
                self.remove_expense(month, index)
            else:
                Write.Print(f"\n No expenses found for {month}", Colors.red_to_yellow, interval=0.05)
        except ValueError:
            Write.Print("\n Invalid index entered. Please enter a numeric value.", Colors.red_to_yellow, interval=0.05)
        except Exception as e:
            Write.Print(f"\n Error in remove expense menu: {e}", Colors.red_to_yellow, interval=0.05)

def main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        tracker = ExpenseTracker(user_name="Guest")
        tracker.menu()
        return 0
    except KeyboardInterrupt:
        Write.Print("\n\n👋 Program terminated by user", Colors.blue_to_purple, interval=0.02)
        return 1
    except Exception as e:
        Write.Print(f"\n❌ An error occurred: {e}", Colors.red_to_yellow, interval=0.02)
        return 1

if __name__ == "__main__":
    sys.exit(main())
