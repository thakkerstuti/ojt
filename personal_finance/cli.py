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