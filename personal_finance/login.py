import os
import csv
import re
import hashlib
from getpass import getpass
from datetime import datetime

# Force Python to always read/write CSV files
# in the same folder as this script.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#               AUTO-CREATE / AUTO-REPAIR CSV HEADERS
def initialize_password_file():
# Defines a function named initialize_password_file.       
    header = ["username", "password"]

    if not os.path.exists("password.csv"):
# If the file "password.csv" does not exist, it creates the file and writes the header row to it.
        with open("password.csv", "w", newline="") as f:
#csv.writer(f) = This creates a CSV writer object that knows how to write rows into the file f.writerow(header) = This tells the writer to write one row in the CSV file.
            csv.writer(f).writerow(header)
        return

    with open("password.csv", "r") as f:
        lines = [line.strip() for line in f.readlines()]

    if len(lines) == 0:
#File exists but is empty (0 lines). Re-create the file and write the correct header
        with open("password.csv", "w", newline="") as f:
            csv.writer(f).writerow(header)
        return

    first_row = lines[0].split(",")
#If the first row of the existing file does not match the expected header, it rewrites the file with the correct header and preserves any valid data rows.
    if first_row != header:
        with open("password.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
#Write correct header again.Re-add old contents below the corrected header. This stops data loss.
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


def initialize_all_files():
    initialize_password_file()
    initialize_userdata_file()
    initialize_expense_file()


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

#Already user login 

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


def register_user():
    print("\nUSER REGISTRATION\n")

    first_name = get_input("Enter First Name: ", is_valid_name)
    last_name = get_input("Enter Last Name: ", is_valid_name)
    age = get_input("Enter Age: ", is_valid_age)
    email = get_input("Enter Email: ", is_valid_email)

    while True:
        username = input("Create a Username: ").strip()
        if username_exists(username):
            print("Username already exists.\n")
        else:
            break

    while True:
        password = getpass("Create a Password: ")
        errors = is_valid_password(password)
        if errors:
            for err in errors:
                print(err)
            print()
        else:
            break

    with open("userdata.csv", "a", newline="") as f:
        csv.writer(f).writerow([first_name, last_name, age, email, username])

    encrypted = hash_password(password)
    with open("password.csv", "a", newline="") as f:
        csv.writer(f).writerow([username, encrypted])

    print("\nRegistration successful!\n")
    finance_menu()


def login_user():
    print("\n<- USER LOGIN ->\n")
    username = input("Enter Username: ").strip()
    password = getpass("Enter Password: ")

    encrypted = hash_password(password)

    with open("password.csv", "r") as f:
        for row in csv.reader(f):
            if row and row[0] == username and row[1] == encrypted:
                print(f"\nLogin Successful! Welcome, {username}.\n")
                finance_menu()
                return

    print("Incorrect username or password.\n")



def add_expense():
    print("\n--- Add New Expense ---")
    amount = input("Enter amount: ").strip()
    category = input("Enter category (Food/Travel/Shopping/Bills/Other): ").strip()
    description = input("Enter description: ").strip()
    payment = input("Enter payment mode (Cash/UPI/Card): ").strip()
    date = datetime.now().strftime("%Y-%m-%d")

    with open("expenses.csv", "a", newline="") as f:
        csv.writer(f).writerow([date, amount, category, description, payment])

    print("Expense added.\n")


def view_expenses():
    print("\n--- All Expenses ---")
    if not os.path.exists("expenses.csv"):
        print("expenses.csv missing\n")
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


def edit_delete_expense():
    print("\n--- Edit/Delete Expense ---")

    with open("expenses.csv", "r") as f:
        rows = list(csv.reader(f))

    if len(rows) <= 1:
        print("No expenses found.\n")
        return

    for i, row in enumerate(rows[1:], start=1):
        print(f"{i}. {row}")

    try:
        choice = int(input("Choose index: "))
    except:
        print("Invalid\n")
        return

    if choice < 1 or choice >= len(rows):
        print("Invalid index\n")
        return

    entry = rows[choice]

    print("1. Edit\n2. Delete")
    action = input("Choose: ").strip()

    if action == "2":
        rows.pop(choice)
        print("Deleted.\n")

    elif action == "1":
        date, amt, cat, desc, mode = entry
        amt2 = input(f"Amount ({amt}): ").strip() or amt
        cat2 = input(f"Category ({cat}): ").strip() or cat
        desc2 = input(f"Description ({desc}): ").strip() or desc
        mode2 = input(f"Payment ({mode}): ").strip() or mode

        rows[choice] = [date, amt2, cat2, desc2, mode2]

        print("Updated.\n")

    with open("expenses.csv", "w", newline="") as f:
        csv.writer(f).writerows(rows)


def monthly_summary():
    print("\n--- Monthly Summary ---")
    month = datetime.now().strftime("%Y-%m")
    total = 0.0

    with open("expenses.csv", "r") as f:
        for row in csv.DictReader(f):
            try:
                if row["date"].startswith(month):
                    total += float(row["amount"])
            except:
                pass

    print(f"Total for {month}: {total}\n")



def finance_menu():
    while True:
        print("\nWhat would you like to do?")
        print("1. Add a new expense")
        print("2. View expenses")
        print("3. Edit/Delete an expense")
        print("4. View monthly summary")
        print("5. Logout")

        ch = input("Enter choice: ").strip()

        if ch == "1":
            add_expense()
        elif ch == "2":
            view_expenses()
        elif ch == "3":
            edit_delete_expense()
        elif ch == "4":
            monthly_summary()
        elif ch == "5":
            print("Logged out.\n")
            break
        else:
            print("Invalid option.\n")


def main():
    while True:
        print("1. New User & Want to Register")
        print("2. Account Already Exists & Ready To Login")
        print("3. Exit\n")

        ch = input("Choose an option (1/2/3): ").strip()

        if ch == "1":
            register_user()
        elif ch == "2":
            login_user()
        elif ch == "3":
            print("Thank you!")
            break
        else:
            print("Invalid option.\n")

initialize_all_files()
main()