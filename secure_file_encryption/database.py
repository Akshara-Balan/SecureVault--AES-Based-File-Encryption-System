# secure_file_encryption/database.py

import json
import os

USER_DB = "users.json"

# Load user data
def load_users():
    if not os.path.exists(USER_DB):
        return {}
    with open(USER_DB, "r") as f:
        return json.load(f)

# Save user data
def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# Save encrypted/decrypted file record
def save_user_file(username, filename, file_type):
    users = load_users()
    if username in users:
        users[username]["files"].append({"name": filename, "type": file_type})
        save_users(users)

# Get user files
def load_user_files(username):
    users = load_users()
    return users.get(username, {}).get("files", [])
