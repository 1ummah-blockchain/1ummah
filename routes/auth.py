# routes/auth.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from firestore_db import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    user_ref = db.collection("users").document(email)
    if user_ref.get().exists:
        return jsonify({"message": "User already exists."}), 409

    hashed = generate_password_hash(password)
    user_ref.set({
        "password": hashed,
        "wallet": None,
        "kyc": False,
        "referral": None
    })

    return jsonify({"message": "User registered successfully."}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user_ref = db.collection("users").document(email)
    user_doc = user_ref.get()

    if not user_doc.exists:
        return jsonify({"message": "Invalid credentials."}), 401

    user_data = user_doc.to_dict()
    if not check_password_hash(user_data["password"], password):
        return jsonify({"message": "Invalid credentials."}), 401

    return jsonify({"message": "Login successful.", "email": email}), 200
