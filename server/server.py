import os
import json
from flask import Flask, request, jsonify
from tools.store import store_user_data
from tools.fetch import fetch_all_users

app = Flask(__name__)

# Ensure the data directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)


@app.route('/store_user_data', methods=['POST'])
def handle_store_user_data():
    """
    MCP endpoint for storing user data.
    Expects JSON: {"name": "...", "email": "...", "dob": "..."}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    name = data.get('name')
    email = data.get('email')
    dob = data.get('dob')

    if not all([name, email, dob]):
        return jsonify({"error": "Missing name, email, or dob"}), 400

    try:
        store_user_data(name, email, dob)
        return jsonify({"status": "success", "message": f"User '{name}' registered successfully."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/fetch_all_users', methods=['POST']) # Using POST as function calls often imply data transfer
def handle_fetch_all_users():
    """
    MCP endpoint for fetching all registered users.
    """
    try:
        users = fetch_all_users()
        return jsonify({"status": "success", "users": users}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("Starting MCP Server on http://127.0.0.1:5000")
    app.run(debug=True) # debug=True will restart server on code changes
