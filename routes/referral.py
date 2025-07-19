from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import sqlite3
from blockchain.config import REFERRAL_BONUS_PERCENT

referral_bp = Blueprint("referral", __name__)
DB_PATH = "data/database.db"

@referral_bp.route("/api/referral", methods=["GET"])
def get_referral_info():
    email = request.args.get("email")
    if not email:
        return jsonify({"message": "Email is required"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # تحقق من وجود المستخدم
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"message": "User not found"}), 404

        # حساب عدد الإحالات التي وصلت للدورة 30 أو أكثر
        cursor.execute("""
            SELECT COUNT(*) FROM users
            WHERE referral = ? AND mining_cycles >= 30
        """, (email,))
        result = cursor.fetchone()
        total_referrals = result[0] if result else 0

        # حساب إجمالي المكافآت
        total_bonus = int(total_referrals * 3 * REFERRAL_BONUS_PERCENT)

        referral_link = f"https://www.1ummah.me/register.html?ref={email}"

        return jsonify({
            "referral_link": referral_link,
            "total_referrals": total_referrals,
            "total_bonus": total_bonus,
            "next_payout": (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
        })

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        conn.close()
