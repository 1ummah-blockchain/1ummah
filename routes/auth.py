from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
import sqlite3

auth_bp = Blueprint('auth', __name__)

DB_PATH = 'database.sqlite3'  # تأكد إن ملف قاعدة البيانات موجود

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return jsonify({"success": False, "message": "User already exists."}), 409

    hashed = generate_password_hash(password)
    cursor.execute("""
        INSERT INTO users (email, password, wallet, kyc, referral, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (email, hashed, None, 0, None, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "User registered successfully."}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

    if not check_password_hash(user["password"], password):
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "email": user["email"],
        "wallet": user["wallet"],
        "kyc": bool(user["kyc"])
    }), 200
