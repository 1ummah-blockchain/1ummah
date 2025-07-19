from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from blockchain.blockchain import blockchain
from blockchain.transaction import Transaction
import sqlite3

send_routes = Blueprint('send_routes', __name__)

MIN_TRANSFER_AMOUNT = 21
TRANSFER_INTERVAL_HOURS = 24
DB_PATH = "database.db"  # تأكد أن قاعدة البيانات بهذا الاسم موجودة

@send_routes.route('/api/send', methods=['POST'])
def send_coins():
    data = request.get_json()
    email = data.get("email")
    sender = data.get("sender")
    recipient = data.get("recipient")
    amount = data.get("amount")

    if not email or not sender or not recipient or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # التحقق من KYC
    cursor.execute("SELECT kyc FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if not user or not user[0]:
        conn.close()
        return jsonify({"success": False, "message": "❌ KYC verification required."}), 403

    # التحقق من الحد الأدنى
    if amount < MIN_TRANSFER_AMOUNT:
        conn.close()
        return jsonify({"success": False, "message": "❌ Minimum transfer is 21 UMH."}), 400

    # التحقق من وقت آخر تحويل
    cursor.execute("SELECT last_transfer FROM transfers WHERE email = ?", (email,))
    row = cursor.fetchone()
    if row:
        last_time = datetime.fromisoformat(row[0])
        now = datetime.utcnow()
        hours_passed = (now - last_time).total_seconds() / 3600
        if hours_passed < TRANSFER_INTERVAL_HOURS:
            conn.close()
            remaining = TRANSFER_INTERVAL_HOURS - hours_passed
            return jsonify({
                "success": False,
                "message": f"⏳ Please wait {remaining:.1f} hours before next transfer."
            })

    # إنشاء المعاملة
    tx = Transaction(sender=sender, recipient=recipient, amount=amount)
    blockchain.add_transaction(tx)

    # تحديث وقت آخر تحويل
    now_str = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO transfers (email, last_transfer)
        VALUES (?, ?)
        ON CONFLICT(email) DO UPDATE SET last_transfer=excluded.last_transfer
    """, (email, now_str))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": f"✅ {amount} UMH sent to {recipient}."}), 200
