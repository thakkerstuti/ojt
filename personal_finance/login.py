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

                    