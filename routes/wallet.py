from flask import Blueprint, request, jsonify
from blockchain.wallet import Wallet  # استدعاء الكلاس من ملف wallet.py

wallet_bp = Blueprint("wallet", __name__)

@wallet_bp.route('/create_wallet', methods=['POST'])
def create_wallet():
    wallet = Wallet()
    return jsonify({
        "address": wallet.address,
        "public_key": wallet.public_key.decode(),
        "private_key": wallet.private_key.decode()
    })
