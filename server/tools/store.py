import os
import csv

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'registration.csv')
# Change 'name' to 'Name' to match the existing CSV header
HEADERS = ["Name", "email", "dob"]

def store_user_data(name: str, email: str, dob: str):
    """
    Stores user registration data in a CSV file.
    Creates the file and writes headers if it doesn't exist.
    """
    file_exists = os.path.exists(DATA_FILE)

    # Ensure the data directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)

        if not file_exists:
            writer.writeheader() # Write headers only if file is new

        # Ensure the dictionary keys also match the capital 'Name' header
        writer.writerow({"Name": name, "email": email, "dob": dob})

    return True # Indicate success
