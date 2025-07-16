# routes/referral.py

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from firestore_db import db
from blockchain.config import REFERRAL_BONUS_PERCENT

referral_bp = Blueprint("referral", __name__)

@referral_bp.route("/api/referral", methods=["GET"])
def get_referral_info():
    email = request.args.get("email")

    if not email:
        return jsonify({"message": "Email is required"}), 400

    user_ref = db.collection("users").document(email)
    user_doc = user_ref.get()

    if not user_doc.exists:
        return jsonify({"message": "User not found"}), 404

    # الحصول على جميع المستخدمين لحساب عدد الإحالات
    users_ref = db.collection("users").stream()
    total_referrals = 0

    for doc in users_ref:
        user_data = doc.to_dict()
        if user_data.get("referral") == email:
            total_referrals += 1

    total_bonus = int(total_referrals * 3 * REFERRAL_BONUS_PERCENT)  # من الدورة 30

    # رابط الإحالة النهائي
    referral_link = f"https://www.1ummah.me/register.html?ref={email}"

    return jsonify({
        "referral_link": referral_link,
        "total_referrals": total_referrals,
        "total_bonus": total_bonus,
        "next_payout": (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
    })
