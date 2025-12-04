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


