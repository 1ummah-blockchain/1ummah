# routes/auth.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

auth_bp = Blueprint('auth', __name__)

USERS_FILE = os.path.join("blockchain", "users.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    users = load_users()
    if email in users:
        return jsonify({"message": "User already exists."}), 409

    hashed = generate_password_hash(password)
    users[email] = {
        "password": hashed,
        "wallet": None,
        "kyc": False,
        "referral": None
    }
    save_users(users)
    return jsonify({"message": "User registered successfully."}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    users = load_users()
    user = users.get(email)

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials."}), 401

    return jsonify({"message": "Login successful.", "email": email}), 200
