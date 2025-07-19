import json
import os
from threading import Lock

DB_PATH = "database/users.json"
lock = Lock()

# إنشاء الملف والمجلد إذا لم يكونا موجودين
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if not os.path.exists(DB_PATH):
    with open(DB_PATH, 'w') as f:
        json.dump({}, f)

def read_users():
    with lock:
        with open(DB_PATH, "r") as f:
            return json.load(f)

def write_users(data):
    with lock:
        with open(DB_PATH, "w") as f:
            json.dump(data, f, indent=4)

def get_user(email):
    users = read_users()
    return users.get(email)

def create_user(email, data):
    users = read_users()
    if email in users:
        return False
    users[email] = data
    write_users(users)
    return True

def update_user(email, data):
    users = read_users()
    users[email] = data
    write_users(users)
    return True
