import os
import csv

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'registration.csv')

def fetch_all_users():
    """
    Fetches all registered users from the CSV file.
    Returns a list of dictionaries, each representing a user.
    """
    users = []
    if not os.path.exists(DATA_FILE):
        return users # Return empty list if file doesn't exist

    with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append(row)
    return users