import time

import json

import hashlib

from .crypto_utils import sign_message, verify_signature, serialize_public_key



class Block:

    def __init__(self, index, previous_hash, transactions, validator, timestamp=None, signature=None):

        self.index = index

        self.timestamp = timestamp or time.time()

        self.transactions = transactions  # قائمة المعاملات (قائمة dicts)

        self.previous_hash = previous_hash

        self.validator = validator  # العنوان العام للمدقق

        self.signature = signature  # التوقيع الرقمي

        self.hash = self.calculate_hash()



    def calculate_hash(self):

        block_string = json.dumps({

            "index": self.index,

            "timestamp": self.timestamp,

            "transactions": self.transactions,

            "previous_hash": self.previous_hash,

            "validator": self.validator

        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()



    def sign_block(self, private_key):

        """

        يوقع البلوك باستخدام المفتاح الخاص للمدقق

        """

        self.signature = sign_message(private_key, self.hash.encode()).hex()



    def to_dict(self):

        return {

            "index": self.index,

            "timestamp": self.timestamp,

            "transactions": self.transactions,

            "previous_hash": self.previous_hash,

            "validator": self.validator,

            "signature": self.signature,

            "hash": self.hash

        }



    @staticmethod

    def from_dict(data):

        return Block(

            index=data["index"],

            timestamp=data["timestamp"],

            transactions=data["transactions"],

            previous_hash=data["previous_hash"],

            validator=data["validator"],

            signature=data.get("signature")

          )
