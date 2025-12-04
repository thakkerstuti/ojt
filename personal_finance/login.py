import os
import csv
import re
import hashlib
from getpass import getpass
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def initialize_password_file():
    header = ["username", "password"]
    if not os.path.exists("password.csv"):
        with open("password.csv", "w", newline="") as f:
            csv.writer(f).writerow(header)
        return

    with open("password.csv", "r") as f:
        lines = [line.strip() for line in f.readlines()]

    if len(lines) == 0:
        with open("password.csv", "w", newline="") as f:
            csv.writer(f).writerow(header)
        return

    first_row = lines[0].split(",")
    if first_row != header:
        with open("password.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for line in lines:
                if line.strip():
                    writer.writerow(line.split(","))


def initialize_userdata_file():
    header = ["First Name", "Last Name", "Age", "Email", "Username"]
    if not os.path.exists("userdata.csv"):
        with open("userdata.csv", "w", newline="") as f:
            csv.writer(f).writerow(header)
        return

    with open("userdata.csv", "r") as f:
        lines = [line.strip() for line in f.readlines()]

    if len(lines) == 0:
        with open("userdata.csv", "w", newline="") as f:
            csv.writer(f).writerow(header)
        return

    first_row = lines[0].split(",")
    if first_row != header:
        with open("userdata.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for line in lines:
                if line.strip():
                    writer.writerow(line.split(","))


def initialize_expense_file():
    header = ["date", "amount", "category", "description", "payment_mode"]
    if not os.path.exists("expenses.csv"):
        with open("expenses.csv", "w", newline="") as f:
            csv.writer(f).writerow(header)
        return

    with open("expenses.csv", "r") as f:
        lines = [line.strip() for line in f.readlines()]

    if len(lines) == 0:
        with open("expenses.csv", "w", newline="") as f:
            csv.writer(f).writerow(header)
        return

    first_row = lines[0].split(",")
    if first_row != header:
        with open("expenses.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for line in lines:
                if line.strip():
                    writer.writerow(line.split(","))


def initialize_budget_file():
    """
    budget.csv columns:
      username, year-month (YYYY-MM), budget_amount, alerted_50, alerted_80, alerted_exceeded
    """
    header = ["username", "month", "budget_amount", "alerted_50", "alerted_80", "alerted_exceeded"]
    if not os.path.exists("budget.csv"):
        with open("budget.csv", "w", newline="") as f:
            csv.writer(f).writerow(header)
        return

    with open("budget.csv", "r") as f:
        lines = [line.strip() for line in f.readlines()]

    if len(lines) == 0:
        with open("budget.csv", "w", newline="") as f:
            csv.writer(f).writerow(header)
        return

    first_row = lines[0].split(",")
    if first_row != header:
        with open("budget.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for line in lines:
                if line.strip():
                    writer.writerow(line.split(","))

                    
def initialize_savings_file():
    """
    savings.csv columns:
      username, goal_id, goal_name, target_amount, current_amount, created_on
    """
    header = ["username", "goal_id", "goal_name", "target_amount", "current_amount", "created_on"]
    if not os.path.exists("savings.csv"):
        with open("savings.csv", "w", newline="") as f:
            csv.writer(f).writerow(header)
        return

    with open("savings.csv", "r") as f:
        lines = [line.strip() for line in f.readlines()]

    if len(lines) == 0:
        with open("savings.csv", "w", newline="") as f:
            csv.writer(f).writerow(header)
        return

    first_row = lines[0].split(",")
    if first_row != header:
        with open("savings.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for line in lines:
                if line.strip():
                    writer.writerow(line.split(","))


def initialize_all_files():
    initialize_password_file()
    initialize_userdata_file()
    initialize_expense_file()
    initialize_budget_file()
    initialize_savings_file()


def is_valid_name(name):
    errors = []
    if not name.isalpha():
        errors.append("Name must contain only alphabets.")
    if len(name) < 3:
        errors.append("Name must be at least 3 characters long.")
    return errors

def is_valid_age(age):
    errors = []
    if not age.isdigit():
        errors.append("Age must be a number.")
        return errors
    age = int(age)
    if age < 15:
        errors.append("User must be at least 15 years old.")
    if age > 80:
        errors.append("Age cannot be more than 80.")
    return errors

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    errors = []
    if not re.match(pattern, email):
        errors.append("Invalid email format. Example: name@example.com")
    return errors

def is_valid_password(password):
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters.")
    if not re.search(r"[A-Za-z]", password):
        errors.append("Password must contain at least one letter.")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special symbol.")
    return errors

def get_input(prompt, validator_function):
    while True:
        value = input(prompt).strip()
        errors = validator_function(value)
        if not errors:
            return value
        for err in errors:
            print(err)
        print()                    


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def username_exists(username):
    if not os.path.exists("password.csv"):
        return False
    with open("password.csv", "r") as f:
        for row in csv.reader(f):
            if row and row[0] == username:
                return True
    return False


def get_current_month():
    return datetime.now().strftime("%Y-%m")


def read_user_budget(username, month=None):
    """
    Return a dict for the user's budget for the given month or None.
    dict keys: month, budget_amount(float), alerted_50, alerted_80, alerted_exceeded
    """
    if month is None:
        month = get_current_month()

    if not os.path.exists("budget.csv"):
        return None

    with open("budget.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("username") == username and row.get("month") == month:
                try:
                    return {
                        "month": row["month"],
                        "budget_amount": float(row["budget_amount"]),
                        "alerted_50": row.get("alerted_50", "no"),
                        "alerted_80": row.get("alerted_80", "no"),
                        "alerted_exceeded": row.get("alerted_exceeded", "no"),
                    }
                except:
                    return None
    return None


def write_user_budget(username, month, budget_amount,
                      alerted_50="no", alerted_80="no", alerted_exceeded="no"):
    """
    Upsert the user's budget for a month.
    """
    rows = []
    header = ["username", "month", "budget_amount", "alerted_50", "alerted_80", "alerted_exceeded"]

    if os.path.exists("budget.csv"):
        with open("budget.csv", "r") as f:
            rows = list(csv.reader(f))

    found = False
    new_rows = []
    if rows:
        new_rows.append(rows[0])
        for r in rows[1:]:
            if len(r) >= 2 and r[0] == username and r[1] == month:
                new_rows.append([username, month, str(budget_amount), alerted_50, alerted_80, alerted_exceeded])
                found = True
            else:
                new_rows.append(r)
    if not rows:
        new_rows.append(header)

    if not found:
        new_rows.append([username, month, str(budget_amount), alerted_50, alerted_80, alerted_exceeded])

    with open("budget.csv", "w", newline="") as f:
        csv.writer(f).writerows(new_rows)


def get_user_savings_goals(username):
    """
    Return list of goals as dicts:
    {goal_id (int), goal_name, target_amount(float), current_amount(float), created_on}
    """
    goals = []
    if not os.path.exists("savings.csv"):
        return goals

    with open("savings.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("username") == username:
                try:
                    goals.append({
                        "goal_id": int(row.get("goal_id", "0")),
                        "goal_name": row.get("goal_name"),
                        "target_amount": float(row.get("target_amount", "0")),
                        "current_amount": float(row.get("current_amount", "0")),
                        "created_on": row.get("created_on")
                    })
                except:
                    pass
    return goals


def write_user_savings_goals(username, goals_list):
    """
    goals_list: list of dicts with keys goal_id, goal_name, target_amount, current_amount, created_on
    This overwrites the user's goals entries in savings.csv (keeps other users intact).
    """
    rows = []
    header = ["username", "goal_id", "goal_name", "target_amount", "current_amount", "created_on"]

    if os.path.exists("savings.csv"):
        with open("savings.csv", "r") as f:
            rows = list(csv.reader(f))

    new_rows = []
    if rows:
        new_rows.append(rows[0])
        for r in rows[1:]:
            if r and r[0] != username:
                new_rows.append(r)
    else:
        new_rows.append(header)

    for g in goals_list:
        new_rows.append([
            username,
            str(g["goal_id"]),
            g["goal_name"],
            str(g["target_amount"]),
            str(g["current_amount"]),
            g.get("created_on", datetime.now().date().isoformat())
        ])

    with open("savings.csv", "w", newline="") as f:
        csv.writer(f).writerows(new_rows)


initialize_all_files()



def change_password(username):
    print("\n--- CHANGE PASSWORD ---\n")

    old_pw = getpass("Enter current password: ")
    encrypted_old = hash_password(old_pw)

    valid = False
    rows = []
    with open("password.csv", "r") as f:
        rows = list(csv.reader(f))

    for row in rows:
        if row and row[0] == username and row[1] == encrypted_old:
            valid = True
            break

    if not valid:
        print("Incorrect current password.\n")
        return

    while True:
        new_pw = getpass("Enter new password: ")
        errors = is_valid_password(new_pw)
        if errors:
            for err in errors:
                print(err)
            continue

        confirm_pw = getpass("Confirm new password: ")
        if new_pw != confirm_pw:
            print("Passwords do not match.\n")
            continue

        break

    encrypted_new = hash_password(new_pw)

    new_rows = []
    for row in rows:
        if row and row[0] == username:
            new_rows.append([username, encrypted_new])
        else:
            new_rows.append(row)

    with open("password.csv", "w", newline="") as f:
        csv.writer(f).writerows(new_rows)

    print("Password successfully changed!\n")



def set_or_update_budget(username):
    print("\n--- SET / UPDATE MONTHLY BUDGET ---\n")
    month = get_current_month()

    existing = read_user_budget(username, month)
    if existing:
        print(f"Current budget for {month}: ₹{existing['budget_amount']}")
    else:
        print(f"No budget set for {month} yet.")

    while True:
        amount = input("Enter monthly budget amount: ").strip()
        try:
            amount = float(amount)
            if amount <= 0:
                print("Budget must be greater than zero.")
                continue
            break
        except:
            print("Enter a valid number.")

    write_user_budget(
        username,
        month,
        amount,
        alerted_50="no",
        alerted_80="no",
        alerted_exceeded="no"
    )

    print(f"Budget for {month} set to ₹{amount}\n")


def calculate_monthly_spending(username):
    month = get_current_month()
    total = 0.0

    if not os.path.exists("expenses.csv"):
        return 0.0

    with open("expenses.csv", "r") as f:
        rows = list(csv.reader(f))

    for row in rows[1:]:
        if len(row) < 2:
            continue
        date_str = row[0]
        try:
            amount = float(row[1])
        except:
            continue

        if date_str.startswith(month):
            total += amount

    return total


def check_budget_alerts(username):
    month = get_current_month()
    budget = read_user_budget(username, month)

    if not budget:
        return

    spent = calculate_monthly_spending(username)
    limit = budget["budget_amount"]

    if limit <= 0:
        return

    a50 = budget.get("alerted_50", "no")
    a80 = budget.get("alerted_80", "no")
    a100 = budget.get("alerted_exceeded", "no")

    percent = (spent / limit) * 100

    updated = False

    if percent >= 50 and a50 == "no":
        print("You have crossed 50% of your monthly budget!")
        budget["alerted_50"] = "yes"
        updated = True

    if percent >= 80 and a80 == "no":
        print("You have crossed 80% of your monthly budget!")
        budget["alerted_80"] = "yes"
        updated = True

    if percent >= 100 and a100 == "no":
        print("You have EXCEEDED your monthly budget!")
        budget["alerted_exceeded"] = "yes"
        updated = True

    if updated:
        write_user_budget(
            username,
            month,
            budget["budget_amount"],
            budget["alerted_50"],
            budget["alerted_80"],
            budget["alerted_exceeded"]



 def create_savings_goal(username):
    print("\n--- CREATE SAVINGS GOAL ---\n")
    goal_name = input("Enter goal name (e.g., New Phone, Laptop, Trip): ").strip()

    while True:
        target = input("Enter target amount: ").strip()
        try:
            target = float(target)
            if target <= 0:
                print("Target must be greater than zero.")
                continue
            break
        except:
            print("Enter a valid number.")

    goals = get_user_savings_goals(username)

    new_id = 1
    if goals:
        new_id = max(g["goal_id"] for g in goals) + 1

    goals.append({
        "goal_id": new_id,
        "goal_name": goal_name,
        "target_amount": target,
        "current_amount": 0.0,
        "created_on": datetime.now().strftime("%Y-%m-%d")
    })

    write_user_savings_goals(username, goals)

    print(f"Savings goal '{goal_name}' created with target ₹{target}\n")


def view_savings_goals(username):
    print("\n--- YOUR SAVINGS GOALS ---\n")
    goals = get_user_savings_goals(username)

    if not goals:
        print("No savings goals found.\n")
        return

    for g in goals:
        print(f"ID: {g['goal_id']}")
        print(f"Goal Name: {g['goal_name']}")
        print(f"Target: ₹{g['target_amount']}")
        print(f"Saved: ₹{g['current_amount']}")
        print(f"Remaining: ₹{g['target_amount'] - g['current_amount']}")
        print("-----------------------------")


def add_money_to_savings(username):
    print("\n--- ADD MONEY TO SAVINGS GOAL ---\n")
    goals = get_user_savings_goals(username)

    if not goals:
        print("No goals exist. Create one first.\n")
        return

    for g in goals:
        print(f"{g['goal_id']}. {g['goal_name']} — Saved ₹{g['current_amount']} / ₹{g['target_amount']}")

    while True:
        try:
            goal_id = int(input("Enter goal ID to add money: ").strip())
            break
        except:
            print("Invalid ID.")

    selected = None
    for g in goals:
        if g["goal_id"] == goal_id:
            selected = g
            break

    if not selected:
        print("Goal not found.\n")
        return

    while True:
        amount = input("Enter amount to add: ").strip()
        try:
            amount = float(amount)
            if amount <= 0:
                print("Enter a positive number.")
                continue
            break
        except:
            print("Invalid amount.")

    selected["current_amount"] += amount

    write_user_savings_goals(username, goals)

    print(f"Added ₹{amount} to '{selected['goal_name']}'")
    print(f"Progress: ₹{selected['current_amount']} / ₹{selected['target_amount']}\n")


def delete_savings_goal(username):
    print("\n--- DELETE SAVINGS GOAL ---\n")
    goals = get_user_savings_goals(username)

    if not goals:
        print("No goals to delete.\n")
        return

    for g in goals:
        print(f"{g['goal_id']}. {g['goal_name']} (Saved ₹{g['current_amount']})")

    while True:
        try:
            goal_id = int(input("Enter goal ID to delete: ").strip())
            break
        except:
            print("Invalid ID.")

    new_goals = [g for g in goals if g["goal_id"] != goal_id]

    write_user_savings_goals(username, new_goals)

    print("Goal deleted successfully.\n")


def savings_menu(username):
    """ Sub-menu for savings feature """
    while True:
        print("\n--- SAVINGS MENU ---")
        print("1. Create Savings Goal")
        print("2. View Savings Goals")
        print("3. Add Money to Goal")
        print("4. Delete Goal")
        print("5. Back to Main Menu")

        ch = input("Choose: ").strip()

        if ch == "1":
            create_savings_goal(username)
        elif ch == "2":
            view_savings_goals(username)
        elif ch == "3":
            add_money_to_savings(username)
        elif ch == "4":
            delete_savings_goal(username)
        elif ch == "5":
            break
        else:
            print("Invalid choice.\n")


def export_expenses(username):
    print("\n--- EXPORT EXPENSES ---\n")

    export_name = f"exported_expenses_{username}.csv"

    if not os.path.exists("expenses.csv"):
        print("No expenses found.\n")
        return

    with open("expenses.csv", "r") as f:
        rows = list(csv.reader(f))

    header = rows[0]
    user_rows = [header]

    user_rows.extend(rows[1:])

    with open(export_name, "w", newline="") as f:
        csv.writer(f).writerows(user_rows)

    print(f"Expenses successfully exported to {export_name}\n")


def add_expense(username):
    print("\n--- ADD NEW EXPENSE ---")

    while True:
        amount = input("Enter amount: ").strip()
        try:
            amount = float(amount)
            break
        except:
            print("Enter a valid number.")

    category = input("Enter category (Food/Travel/Shopping/Bills/Other): ").strip()
    description = input("Enter description: ").strip()
    payment = input("Enter payment mode (Cash/UPI/Card): ").strip()
    date = datetime.now().strftime("%Y-%m-%d")

    with open("expenses.csv", "a", newline="") as f:
        csv.writer(f).writerow([date, amount, category, description, payment])

    print("Expense added.\n")

    check_budget_alerts(username)


def view_expenses(username):
    print("\n--- ALL EXPENSES ---")

    if not os.path.exists("expenses.csv"):
        print("No expenses found.\n")
        return

    with open("expenses.csv", "r") as f:
        rows = list(csv.reader(f))

    if len(rows) <= 1:
        print("No expenses recorded yet.\n")
        return

    print("\n#   DATE         AMOUNT   CATEGORY     DESCRIPTION      MODE")
    print("----------------------------------------------------------------")

    for i, row in enumerate(rows[1:], start=1):
        if len(row) < 5:
            continue
        date, amt, cat, desc, mode = row
        print(f"{i}.  {date:<12} {amt:<8} {cat:<12} {desc:<15} {mode}")



def edit_delete_expense(username):
    print("\n--- EDIT/DELETE EXPENSE ---")

    if not os.path.exists("expenses.csv"):
        print("No expenses found.\n")
        return

    with open("expenses.csv", "r") as f:
        rows = list(csv.reader(f))

    if len(rows) <= 1:
        print("No expenses to modify.\n")
        return

    for i, row in enumerate(rows[1:], start=1):
        print(f"{i}. {row}")

    try:
        choice = int(input("Choose index: "))
    except:
        print("Invalid input.\n")
        return

    if choice < 1 or choice >= len(rows):
        print("Invalid index.\n")
        return

    entry = rows[choice]
    date, amt, cat, desc, mode = entry  

    
             