# routes/send.py

from flask import Blueprint, request, jsonify
from datetime import datetime
from blockchain.blockchain import blockchain
from blockchain.transaction import Transaction
import json
import os

send_routes = Blueprint('send_routes', __name__)

MIN_TRANSFER_AMOUNT = 21
TRANSFER_INTERVAL_HOURS = 24
TRANSFER_LOG_PATH = 'data/transfer_log.json'
KYC_DATA_PATH = 'data/kyc_status.json'


# تحميل سجلات التحويل
def load_transfer_log():
    if not os.path.exists(TRANSFER_LOG_PATH):
        with open(TRANSFER_LOG_PATH, 'w') as f:
            json.dump({}, f)
    with open(TRANSFER_LOG_PATH, 'r') as f:
        return json.load(f)

def save_transfer_log(data):
    with open(TRANSFER_LOG_PATH, 'w') as f:
        json.dump(data, f, indent=2)


# التحقق من حالة KYC
def is_user_verified(email):
    if not os.path.exists(KYC_DATA_PATH):
        return False
    with open(KYC_DATA_PATH, 'r') as f:
        data = json.load(f)
    return data.get(email) == "verified"


@send_routes.route('/api/send', methods=['POST'])
def send_coins():
    data = request.get_json()
    email = data.get("email")
    sender = data.get("sender")
    recipient = data.get("recipient")
    amount = data.get("amount")

    if not email or not sender or not recipient or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    # التحقق من حالة KYC
    if not is_user_verified(email):
        return jsonify({"success": False, "message": "❌ KYC verification required."}), 403

    # التحقق من الحد الأدنى للمبلغ
    if amount < MIN_TRANSFER_AMOUNT:
        return jsonify({"success": False, "message": "❌ Minimum transfer is 21 UMH."}), 400

    # التحقق من عدد مرات التحويل
    log = load_transfer_log()
    last_time = log.get(email)

    if last_time:
        last_dt = datetime.fromisoformat(last_time)
        now = datetime.utcnow()
        hours_passed = (now - last_dt).total_seconds() / 3600
        if hours_passed < TRANSFER_INTERVAL_HOURS:
            remaining = TRANSFER_INTERVAL_HOURS - hours_passed
            return jsonify({
                "success": False,
                "message": f"⏳ Please wait {remaining:.1f} hours before next transfer."
            })

    # إنشاء معاملة جديدة
    tx = Transaction(sender=sender, recipient=recipient, amount=amount)
    blockchain.add_transaction(tx)

    # تحديث سجل التحويل
    log[email] = datetime.utcnow().isoformat()
    save_transfer_log(log)

    return jsonify({"success": True, "message": f"✅ {amount} UMH sent to {recipient}."}), 200
