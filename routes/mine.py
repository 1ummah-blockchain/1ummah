from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from blockchain.blockchain import blockchain
from blockchain.transaction import Transaction
from blockchain.referral import get_referral_bonus_transaction
import json
import os

mine_routes = Blueprint('mine_routes', __name__)

MINING_REWARD = 3
MINING_INTERVAL_HOURS = 24
USER_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')

# التأكد من وجود مجلد data
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data'), exist_ok=True)

def load_users():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

@mine_routes.route('/api/mine/status', methods=['GET'])
def check_mining_status():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    users = load_users()
    user = users.get(email)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    last_mined = user.get("last_mined")
    if last_mined:
        last_time_dt = datetime.fromisoformat(last_mined)
        now = datetime.utcnow()
        hours_passed = (now - last_time_dt).total_seconds() / 3600

        if hours_passed < MINING_INTERVAL_HOURS:
            return jsonify({
                'eligible': False,
                'remaining_hours': round(MINING_INTERVAL_HOURS - hours_passed, 2)
            })

    return jsonify({'eligible': True})

@mine_routes.route('/api/mine', methods=['POST'])
def mine_coins():
    data = request.get_json()
    email = data.get('email')
    wallet = data.get('wallet')
    referrer = data.get('referrer')

    if not email or not wallet:
        return jsonify({'error': 'Email and wallet are required'}), 400

    users = load_users()
    user = users.get(email)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # التحقق من إثبات النشاط
    if not user.get("activity_verified", False):
        return jsonify({'success': False, 'message': '❌ Please confirm your activity before mining.'}), 403

    last_mined = user.get("last_mined")
    if last_mined:
        last_time_dt = datetime.fromisoformat(last_mined)
        now = datetime.utcnow()
        hours_passed = (now - last_time_dt).total_seconds() / 3600
        if hours_passed < MINING_INTERVAL_HOURS:
            return jsonify({'success': False, 'message': '⏳ Please wait before next mining.'})

    # إنشاء معاملة التعدين
    reward_tx = Transaction(sender="COINBASE", recipient=wallet, amount=MINING_REWARD)
    blockchain.add_transaction(reward_tx)

    # مكافأة الإحالة
    if referrer:
        bonus_tx = get_referral_bonus_transaction(referrer_address=referrer, miner_address=wallet)
        if bonus_tx:
            blockchain.add_transaction(bonus_tx)

    # تحديث المستخدم
    users[email]["last_mined"] = datetime.utcnow().isoformat()
    users[email]["activity_verified"] = False
    save_users(users)

    return jsonify({'success': True, 'message': '🎉 You earned 3 UMH!'}), 200
