# routes/mine.py

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
MINING_LOG_PATH = 'data/mining_log.json'


# تحميل بيانات التعدين أو إنشاء ملف جديد
def load_mining_log():
    if not os.path.exists(MINING_LOG_PATH):
        with open(MINING_LOG_PATH, 'w') as f:
            json.dump({}, f)
    with open(MINING_LOG_PATH, 'r') as f:
        return json.load(f)

def save_mining_log(data):
    with open(MINING_LOG_PATH, 'w') as f:
        json.dump(data, f, indent=2)

@mine_routes.route('/api/mine/status', methods=['GET'])
def check_mining_status():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    log = load_mining_log()
    last_time = log.get(email)

    if last_time:
        last_time_dt = datetime.fromisoformat(last_time)
        now = datetime.utcnow()
        hours_passed = (now - last_time_dt).total_seconds() / 3600

        if hours_passed < MINING_INTERVAL_HOURS:
            return jsonify({
                'eligible': False,
                'remaining_hours': MINING_INTERVAL_HOURS - hours_passed
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

    log = load_mining_log()
    last_time = log.get(email)

    if last_time:
        last_time_dt = datetime.fromisoformat(last_time)
        now = datetime.utcnow()
        hours_passed = (now - last_time_dt).total_seconds() / 3600

        if hours_passed < MINING_INTERVAL_HOURS:
            return jsonify({'success': False, 'message': '⏳ Please wait before next mining.'})

    # إنشاء معاملة التعدين للمستخدم
    reward_tx = Transaction(sender="COINBASE", recipient=wallet, amount=MINING_REWARD)
    blockchain.add_transaction(reward_tx)

    # إنشاء مكافأة الإحالة إن وُجد مرجع صالح
    if referrer:
        bonus_tx = get_referral_bonus_transaction(referrer_address=referrer, miner_address=wallet)
        if bonus_tx:
            blockchain.add_transaction(bonus_tx)

    # تحديث سجل التعدين
    log[email] = datetime.utcnow().isoformat()
    save_mining_log(log)

    return jsonify({'success': True, 'message': '🎉 You earned 3 UMH!'}), 200
