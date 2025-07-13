# blockchain/transaction.py



import json

import time

from .crypto_utils import verify_signature





class Transaction:

    def __init__(self, sender, recipient, amount, timestamp=None, signature=""):

        self.sender = sender

        self.recipient = recipient

        self.amount = amount

        self.timestamp = timestamp if timestamp else int(time.time())

        self.signature = signature



    def to_dict(self):

        return {

            "sender": self.sender,

            "recipient": self.recipient,

            "amount": self.amount,

            "timestamp": self.timestamp,

            "signature": self.signature

        }



    def to_json(self):

        return json.dumps(self.to_dict(), sort_keys=True)



    def sign(self, wallet):

        self.signature = wallet.sign(self.to_json())



    def is_valid(self):

        if self.sender == "COINBASE":

            return True  # مكافآت التعدين لا تحتاج تحقق

        if not self.signature:

            return False

        return verify_signature(self.sender, self.to_json(), self.signature)



    @staticmethod

    def from_dict(data):

        return Transaction(

            sender=data["sender"],

            recipient=data["recipient"],

            amount=data["amount"],

            timestamp=data.get("timestamp"),

            signature=data.get("signature", "")

        )
