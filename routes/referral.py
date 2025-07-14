# routes/referral.py

from flask import Blueprint, jsonify, request
import os
import json
from datetime import datetime, timedelta
from blockchain.config import REFERRAL_BONUS_PERCENT

referral_bp = Blueprint("referral", __name__)

USERS_FILE = os.path.join("blockchain", "users.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

@referral_bp.route("/api/referral", methods=["GET"])
def get_referral_info():
    email = request.args.get("email")

    if not email:
        return jsonify({"message": "Email is required"}), 400

    users = load_users()
    user = users.get(email)

    if not user:
        return jsonify({"message": "User not found"}), 404

    # توليد رابط الإحالة
    referral_link = f"https://your-domain.com/register.html?ref={email}"

    # بيانات افتراضية — يمكنك لاحقًا ربطها من قاعدة بيانات المعاملات
    total_referrals = sum(1 for u in users.values() if u.get("referral") == email)
    total_bonus = total_referrals * 3 * REFERRAL_BONUS_PERCENT  # من الدورة 30
    next_payout = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    return jsonify({
        "referral_link": referral_link,
        "total_referrals": total_referrals,
        "total_bonus": int(total_bonus),
        "next_payout": next_payout
    })
