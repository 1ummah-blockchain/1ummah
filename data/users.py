import os
import json

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

def add_user(username, wallet_data):
    users = load_users()
    if username in users:
        return False  # المستخدم موجود بالفعل
    users[username] = {
        "wallet": wallet_data,
        "kyc": None,
        "mined_coins": 0,
        "referral": None,
        "referral_bonus": 0,
        "mining_count": 0
    }
    save_users(users)
    return True

def get_user(username):
    users = load_users()
    return users.get(username)

def update_user(username, user_data):
    users = load_users()
    users[username] = user_data
    save_users(users)
