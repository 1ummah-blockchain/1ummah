from flask import Flask, request, jsonify
from blockchain.wallet import Wallet
from blockchain.chain import Blockchain
from blockchain.kyc import KYCRegistry
from blockchain.admin import issue_coins, burn_coins
import datetime
import json
import os  # ← تمت إضافته هنا

# إعداد النظام
app = Flask(__name__)
blockchain = Blockchain()
kyc_registry = KYCRegistry()

# قاعدة بيانات مؤقتة لتخزين توقيتات التعدين
last_mining_times = {}

@app.route("/")
def index():
    return "1Ummah Blockchain API is running."

# 🔍 فحص حالة التعدين
@app.route("/api/mine/status", methods=["GET"])
def check_mining_status():
    address = request.args.get("address")
    if not address:
        return jsonify({"error": "Address is required"}), 400

    if not kyc_registry.is_verified(address):
        return jsonify({"eligible": False, "message": "KYC not verified"}), 403

    last_time = last_mining_times.get(address)
    if last_time:
        hours_elapsed = (datetime.datetime.now() - last_time).total_seconds() / 3600
        if hours_elapsed < 24:
            return jsonify({
                "eligible": False,
                "remaining_hours": 24 - hours_elapsed
            })

    return jsonify({"eligible": True})

# ⚒️ تنفيذ التعدين
@app.route("/api/mine", methods=["POST"])
def start_mining():
    data = request.get_json()
    address = data.get("address")
    referrer = data.get("referrer", None)

    if not address:
        return jsonify({"error": "Address required"}), 400

    if not kyc_registry.is_verified(address):
        return jsonify({"success": False, "message": "❌ KYC not verified"}), 403

    last_time = last_mining_times.get(address)
    if last_time:
        hours_elapsed = (datetime.datetime.now() - last_time).total_seconds() / 3600
        if hours_elapsed < 24:
            return jsonify({
                "success": False,
                "message": f"⏳ Try again in {24 - hours_elapsed:.1f} hours"
            }), 403

    block = blockchain.mine_pending_transactions(
        miner_address=address,
        cycle_count=1,
        referrer=referrer
    )

    if block:
        last_mining_times[address] = datetime.datetime.now()
        return jsonify({"success": True, "message": "🎉 Mining successful! You earned 3 UMH."})
    else:
        return jsonify({"success": False, "message": "❌ Mining failed or not allowed yet."}), 400

# 🪙 إصدار عملات (Admin Only)
@app.route("/api/issue", methods=["POST"])
def issue():
    data = request.get_json()
    try:
        tx = issue_coins(
            to_address=data["to"],
            amount=data["amount"],
            caller=data["caller"]
        )
        blockchain.add_transaction(tx)
        return jsonify({"success": True, "message": "✅ Issuance transaction added."})
    except PermissionError as e:
        return jsonify({"success": False, "message": str(e)}), 403

# 🔥 حرق عملات (Admin Only)
@app.route("/api/burn", methods=["POST"])
def burn():
    data = request.get_json()
    try:
        tx = burn_coins(
            from_address=data["from"],
            amount=data["amount"],
            caller=data["caller"]
        )
        blockchain.add_transaction(tx)
        return jsonify({"success": True, "message": "🔥 Burn transaction added."})
    except PermissionError as e:
        return jsonify({"success": False, "message": str(e)}), 403

# ✅ تشغيل التطبيق
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # ← هذا السطر يسمح بالمرونة حسب بيئة التشغيل
    app.run(host="0.0.0.0", port=port)
