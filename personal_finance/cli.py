import csv
import re
import os
import hashlib
from getpass import getpass

def is_valid_name(name):
    return name.isalpha() and len(name) >= 3

def is_valid_age(age):
    return age.isdigit() and 18 <= int(age) <= 80

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    if not re.search(r"[A-Za-z]", password):
        return False
    return True

def get_input(prompt, validation_function):
    while True:
        value = input(prompt)
        if validation_function(value):
            return value
        else:
            print("The input is invalid. Please try again.\n")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def username_exists(username):
    if not os.path.exists("users.csv"):
        return False
    with open("users.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                return True
    return False

def register_user():
    print("\nUSER REGISTRATION")

    first_name = get_input("Enter First Name: ", is_valid_name)
    last_name  = get_input("Enter Last Name: ", is_valid_name)
    age        = get_input("Enter Age: ", is_valid_age)
    email      = get_input("Enter Email: ", is_valid_email)

    while True:
        username = input("Create a Username: ")
        if username_exists(username):
            print("Username already exists. Try again.\n")
        else:
            break

    while True:
        password = getpass("Create a Password: ")
        if is_valid_password(password):
            print("Password accepted!")
            break
        else:
            print("\n You Entered An Invalid password!")
            print("Password must be at least 8 characters long, include:")
            print("- Letters")
            print("- Digits")
            print("- Special characters\n")

    csv_file = 'userdatanew.csv'
    file_exists = os.path.exists(csv_file)

    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["First Name", "Last Name", "Age", "Email"])
        writer.writerow([first_name, last_name, age, email])

    encrypted = hash_password(password)

    with open("users.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, encrypted])

    print("\nRegistration successful!")
    print("You can now login.\n")

def login_user():
    print("\n<-USER LOGIN->")

    username = input("Enter Username: ")
    password = getpass("Enter Password: ")

    if not os.path.exists("users.csv"):
        print("No registered users found. Please register first.")
        return