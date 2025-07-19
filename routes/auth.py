from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from firestore_db import db
from datetime import datetime
import re

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."}), 400
    if not is_valid_email(email):
        return jsonify({"success": False, "message": "Invalid email format."}), 400
    if len(password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters."}), 400

    user_ref = db.collection("users").document(email)
    if user_ref.get().exists:
        return jsonify({"success": False, "message": "User already exists."}), 409

    hashed = generate_password_hash(password)
    user_ref.set({
        "password": hashed,
        "wallet": None,
        "kyc": False,
        "referral": None,
        "created_at": datetime.utcnow().isoformat()
    })

    return jsonify({"success": True, "message": "User registered successfully."}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user_ref = db.collection("users").document(email)
    user_doc = user_ref.get()

    if not user_doc.exists:
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

    user_data = user_doc.to_dict()
    if not check_password_hash(user_data["password"], password):
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "email": email,
        "wallet": user_data.get("wallet"),
        "kyc": user_data.get("kyc")
    }), 200
