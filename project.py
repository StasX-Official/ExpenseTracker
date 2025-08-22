import os
import sys
import json
import csv
from datetime import datetime, timedelta
import time
try:
    from pystyle import Colors, Colorate, Center, Write, Box, Anime, System
except Exception:
    class _Colors:
        blue_to_purple = None
        red_to_yellow = None
        green_to_blue = None
        blue_to_cyan = None
        yellow_to_red = None

    class _Colorate:
        @staticmethod
        def Diagonal(_, text):
            return text

        @staticmethod
        def Horizontal(_, text):
            return text

    class _Write:
        @staticmethod
        def Print(text, *args, **kwargs):
            print(text)

        @staticmethod
        def Input(prompt, *args, **kwargs):
            try:
                return input(prompt)
            except Exception:
                return ""

    class _Box:
        @staticmethod
        def Lines(text):
            return text

    class _Anime:
        @staticmethod
        def Move(*args, **kwargs):
            return None

    class _System:
        @staticmethod
        def Clear():
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
            except Exception:
                pass

    Colors = _Colors()
    Colorate = _Colorate()
    Write = _Write()
    Box = _Box()
    Anime = _Anime()
    System = _System()

def print_banner():
    banner = r"""  _____                                  _____               _
 | ____|_  ___ __   ___ _ __  ___  ___  |_   _| __ __ _  ___| | _____ _ __
 |  _| \ \/ / '_ \ / _ \ '_ \/ __|/ _ \   | || '__/ _` |/ __| |/ / _ \ '__|
 | |___ >  <| |_) |  __/ | | \__ \  __/   | || | | (_| | (__|   <  __/ |
 |_____/_/\_\ .__/ \___|_| |_|___/\___|   |_||_|  \__,_|\___|_|\_\___|_|
            |_|                                                           """
    print(Colorate.Diagonal(Colors.blue_to_purple, banner))
    if not os.environ.get('PYTEST_CURRENT_TEST'):
        try:
            time.sleep(1)
        except Exception:
            pass

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
    if os.environ.get('PYTEST_CURRENT_TEST') or not sys.stdout.isatty():
        return
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
        self.incomes_file = 'incomes.json'

        show_loading_animation()

        self.user_data = self.load_user_data()
        self.expenses = self.load_expenses()
        self.incomes = self.load_incomes()
        self.banner = print_banner

        try:
            if not os.path.exists(self.user_data_path):
                with open(self.user_data_path, 'w') as f:
                    json.dump(self.user_data, f)
            if not os.path.exists(self.expenses_file):
                with open(self.expenses_file, 'w') as f:
                    json.dump(self.expenses, f)
            if not os.path.exists(self.incomes_file):
                with open(self.incomes_file, 'w') as f:
                    json.dump(self.incomes, f)
        except Exception:
            pass

        try:
            current_month = datetime.now().strftime("%Y-%m")
            last_applied = self.user_data.get('last_applied_month')
            if last_applied != current_month:
                self.apply_monthly_recurring(current_month)
                self.user_data['last_applied_month'] = current_month
                self.save_user_data()
        except Exception:
            pass

    def load_incomes(self):
        try:
            if os.path.exists(self.incomes_file):
                with open(self.incomes_file, 'r') as file:
                    return json.load(file)
            else:
                return {}
        except Exception as e:
            Write.Print(f"\n Error loading incomes: {e}", Colors.red_to_yellow, interval=0.05)
            return {}

    def save_incomes(self):
        try:
            with open(self.incomes_file, 'w') as file:
                json.dump(self.incomes, file, indent=4)
        except Exception as e:
            Write.Print(f"\n Error saving incomes: {e}", Colors.red_to_yellow, interval=0.05)

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

    def list_months(self):
        """Return a sorted list of months (YYYY-MM) that have expenses."""
        try:
            return sorted(self.expenses.keys())
        except Exception:
            return []

    def export_month_to_csv(self, month, file_path=None):
        """Export the specified month's expenses to a CSV file and return the path.

        Returns None on failure.
        """
        try:
            if month not in self.expenses:
                raise ValueError("Month not found")
            if not file_path:
                file_path = f"{month}_expenses.csv"
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['date', 'category', 'amount'])
                for exp in self.expenses[month]:
                    writer.writerow([exp.get('date'), exp.get('category'), exp.get('amount')])
            return file_path
        except Exception as e:
            Write.Print(f"\n Error exporting to CSV: {e}", Colors.red_to_yellow, interval=0.05)
            return None

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

    def add_income(self, category, amount, month):
        """Add an income record for a given month."""
        try:
            inc = {
                'category': category,
                'amount': float(amount),
                'date': datetime.now().strftime("%Y-%m-%d")
            }
            if month not in self.incomes:
                self.incomes[month] = []
            self.incomes[month].append(inc)
            self.save_incomes()
            Write.Print("\n Income added successfully!", Colors.green_to_blue, interval=0.05)
        except Exception as e:
            Write.Print(f"\n Error adding income: {e}", Colors.red_to_yellow, interval=0.05)

    def get_total_income(self, month):
        try:
            if month in self.incomes:
                return sum(inc['amount'] for inc in self.incomes[month])
            return 0
        except Exception as e:
            Write.Print(f"\n Error getting total income: {e}", Colors.red_to_yellow, interval=0.05)
            return 0

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

    def view_incomes_by_category(self, month, category):
        try:
            if month in self.incomes:
                filtered = [inc for inc in self.incomes[month] if inc['category'] == category]
                total = sum(inc['amount'] for inc in filtered)
                return filtered, total
            else:
                return [], 0
        except Exception as e:
            Write.Print(f"\n Error viewing incomes by category: {e}", Colors.red_to_yellow, interval=0.05)
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

    def apply_monthly_recurring(self, month):
        """Apply subscriptions (monthly expenses) and fixed salary to the given month.

        This will add subscription entries as expenses and a fixed salary as income
        for the month unless already present (best-effort: check identical amounts/categories).
        """
        try:
            subs = self.user_data.get('subscriptions', [])
            for sub in subs:
                already = any(e.get('category') == sub.get('category') and float(e.get('amount')) == float(sub.get('amount')) for e in self.expenses.get(month, []))
                if not already:
                    self.add_expense(sub.get('category'), float(sub.get('amount')), month)

            fixed = self.user_data.get('fixed_salary')
            if fixed:
                already_inc = any(i.get('category') == 'Salary' and float(i.get('amount')) == float(fixed) for i in self.incomes.get(month, []))
                if not already_inc:
                    self.add_income('Salary', float(fixed), month)
        except Exception as e:
            Write.Print(f"\n Error applying recurring items: {e}", Colors.red_to_yellow, interval=0.05)

    def add_subscription(self, category, amount):
        try:
            subs = self.user_data.setdefault('subscriptions', [])
            subs.append({'category': category, 'amount': float(amount)})
            self.save_user_data()
            Write.Print("\n Subscription added.", Colors.green_to_blue, interval=0.05)
        except Exception as e:
            Write.Print(f"\n Error adding subscription: {e}", Colors.red_to_yellow, interval=0.05)

    def remove_subscription(self, index):
        try:
            subs = self.user_data.get('subscriptions', [])
            if 0 <= index < len(subs):
                subs.pop(index)
                self.save_user_data()
                Write.Print("\n Subscription removed.", Colors.green_to_blue, interval=0.05)
            else:
                Write.Print("\n Invalid subscription index.", Colors.red_to_yellow, interval=0.05)
        except Exception as e:
            Write.Print(f"\n Error removing subscription: {e}", Colors.red_to_yellow, interval=0.05)

    def set_fixed_salary(self, amount):
        try:
            self.user_data['fixed_salary'] = float(amount)
            self.save_user_data()
            Write.Print("\n Fixed salary set.", Colors.green_to_blue, interval=0.05)
        except Exception as e:
            Write.Print(f"\n Error setting fixed salary: {e}", Colors.red_to_yellow, interval=0.05)

    def clear_fixed_salary(self):
        try:
            if 'fixed_salary' in self.user_data:
                del self.user_data['fixed_salary']
                self.save_user_data()
                Write.Print("\n Fixed salary cleared.", Colors.green_to_blue, interval=0.05)
        except Exception as e:
            Write.Print(f"\n Error clearing fixed salary: {e}", Colors.red_to_yellow, interval=0.05)

    def import_csv(self, file_path):
        """Import transactions from a CSV file.

        CSV columns: date,category,amount,kind (optional: expense|income|subscription|salary)
        For 'subscription' rows the subscription will be added to user_data and applied for the month of the date.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    date = row.get('date')
                    category = row.get('category') or 'Imported'
                    amount = float(row.get('amount') or 0)
                    kind = (row.get('kind') or 'expense').lower()
                    month = None
                    try:
                        month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')
                    except Exception:
                        month = datetime.now().strftime('%Y-%m')

                    if kind == 'income' or kind == 'salary':
                        self.add_income(category if kind == 'income' else 'Salary', amount, month)
                    elif kind == 'subscription':
                        self.add_subscription(category, amount)
                        self.add_expense(category, amount, month)
                    else:
                        self.add_expense(category, amount, month)
            Write.Print("\n CSV import completed.", Colors.green_to_blue, interval=0.05)
        except Exception as e:
            Write.Print(f"\n Error importing CSV: {e}", Colors.red_to_yellow, interval=0.05)

    def analytics(self, period='month', reference=None):
        """Return analytics totals for expenses, income, and profit.

        period: 'week', 'month', 'year'
        reference: for 'month' use 'YYYY-MM' (default current), for 'year' use 'YYYY', for 'week' use a date 'YYYY-MM-DD' representing a day in the week.
        Returns dict: { 'expenses': x, 'income': y, 'profit': y - x, 'breakdown': {category: amount, ...} }
        """
        try:
            if period == 'month':
                month = reference or datetime.now().strftime('%Y-%m')
                exp_total = self.get_total_expenses(month)
                inc_total = self.get_total_income(month)
                breakdown = {}
                for m in self.expenses.get(month, []):
                    breakdown[m.get('category')] = breakdown.get(m.get('category'), 0) + float(m.get('amount', 0))
                return {'period': month, 'expenses': exp_total, 'income': inc_total, 'profit': inc_total - exp_total, 'breakdown': breakdown}

            if period == 'year':
                year = reference or datetime.now().strftime('%Y')
                exp_total = 0
                inc_total = 0
                breakdown = {}
                for month_key, items in self.expenses.items():
                    if month_key.startswith(year):
                        for m in items:
                            amt = float(m.get('amount', 0))
                            exp_total += amt
                            breakdown[m.get('category')] = breakdown.get(m.get('category'), 0) + amt
                for month_key, items in self.incomes.items():
                    if month_key.startswith(year):
                        for inc in items:
                            inc_total += float(inc.get('amount', 0))
                return {'period': year, 'expenses': exp_total, 'income': inc_total, 'profit': inc_total - exp_total, 'breakdown': breakdown}

            if period == 'week':
                ref_date = datetime.strptime(reference, '%Y-%m-%d') if reference else datetime.now()
                start = ref_date
                start = ref_date - timedelta(days=ref_date.isoweekday() - 1)
                end = start + timedelta(days=6)
                exp_total = 0
                inc_total = 0
                breakdown = {}
                for month_key, items in self.expenses.items():
                    for m in items:
                        try:
                            d = datetime.strptime(m.get('date'), '%Y-%m-%d')
                            if start.date() <= d.date() <= end.date():
                                amt = float(m.get('amount', 0))
                                exp_total += amt
                                breakdown[m.get('category')] = breakdown.get(m.get('category'), 0) + amt
                        except Exception:
                            continue
                for month_key, items in self.incomes.items():
                    for inc in items:
                        try:
                            d = datetime.strptime(inc.get('date'), '%Y-%m-%d')
                            if start.date() <= d.date() <= end.date():
                                inc_total += float(inc.get('amount', 0))
                        except Exception:
                            continue
                period_label = f"{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}"
                return {'period': period_label, 'expenses': exp_total, 'income': inc_total, 'profit': inc_total - exp_total, 'breakdown': breakdown}

            return {}
        except Exception as e:
            Write.Print(f"\n Error calculating analytics: {e}", Colors.red_to_yellow, interval=0.05)
            return {}

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
