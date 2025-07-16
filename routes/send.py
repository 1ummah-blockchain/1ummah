# routes/send.py

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from blockchain.blockchain import blockchain
from blockchain.transaction import Transaction
from firestore_db import db

send_routes = Blueprint('send_routes', __name__)

MIN_TRANSFER_AMOUNT = 21
TRANSFER_INTERVAL_HOURS = 24

@send_routes.route('/api/send', methods=['POST'])
def send_coins():
    data = request.get_json()
    email = data.get("email")
    sender = data.get("sender")
    recipient = data.get("recipient")
    amount = data.get("amount")

    if not email or not sender or not recipient or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    # تحقق من حالة KYC من قاعدة البيانات
    user_ref = db.collection("users").document(email)
    user_doc = user_ref.get()
    if not user_doc.exists or not user_doc.to_dict().get("kyc"):
        return jsonify({"success": False, "message": "❌ KYC verification required."}), 403

    # التحقق من الحد الأدنى
    if amount < MIN_TRANSFER_AMOUNT:
        return jsonify({"success": False, "message": "❌ Minimum transfer is 21 UMH."}), 400

    # التحقق من وقت آخر تحويل
    transfer_ref = db.collection("transfers").document(email)
    transfer_doc = transfer_ref.get()

    if transfer_doc.exists:
        last_time_str = transfer_doc.to_dict().get("last_transfer")
        last_time = datetime.fromisoformat(last_time_str)
        now = datetime.utcnow()
        hours_passed = (now - last_time).total_seconds() / 3600

        if hours_passed < TRANSFER_INTERVAL_HOURS:
            remaining = TRANSFER_INTERVAL_HOURS - hours_passed
            return jsonify({
                "success": False,
                "message": f"⏳ Please wait {remaining:.1f} hours before next transfer."
            })

    # إنشاء المعاملة
    tx = Transaction(sender=sender, recipient=recipient, amount=amount)
    blockchain.add_transaction(tx)

    # تحديث وقت آخر تحويل
    transfer_ref.set({
        "last_transfer": datetime.utcnow().isoformat()
    })

    return jsonify({"success": True, "message": f"✅ {amount} UMH sent to {recipient}."}), 200
