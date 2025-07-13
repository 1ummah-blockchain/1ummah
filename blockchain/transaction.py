# blockchain/transaction.py

import time
import hashlib
from .crypto_utils import verify_signature

class Transaction:
    def __init__(self, sender, recipient, amount, signature, timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature
        self.timestamp = timestamp or time.time()

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "signature": self.signature,
            "timestamp": self.timestamp
        }

    def compute_hash(self):
        tx_str = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha256(tx_str.encode()).hexdigest()

    @staticmethod
    def is_valid(transaction, user_db):
        # تحقق من التوقيع
        tx_data = f"{transaction.sender}{transaction.recipient}{transaction.amount}{transaction.timestamp}"
        if not verify_signature(transaction.sender, tx_data, transaction.signature):
            return False, "Invalid signature"

        # تحقق من KYC
        sender_data = user_db.get(transaction.sender)
        recipient_data = user_db.get(transaction.recipient)

        if not sender_data or not recipient_data:
            return False, "Sender or recipient does not exist"

        if not sender_data.get("kyc_passed", False) or not recipient_data.get("kyc_passed", False):
            return False, "Sender or recipient has not passed KYC"

        # تحقق من الرصيد
        if sender_data.get("balance", 0) < transaction.amount:
            return False, "Insufficient balance"

        return True, "Transaction is valid"
