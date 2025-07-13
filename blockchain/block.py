# blockchain/block.py

import hashlib
import json
import time
from .crypto_utils import serialize_public_key


class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, creator_address, signature=""):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions  # قائمة المعاملات
        self.creator_address = creator_address
        self.signature = signature
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "creator_address": self.creator_address,
            "signature": self.signature
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "creator_address": self.creator_address,
            "signature": self.signature,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(data):
        return Block(
            data["index"],
            data["previous_hash"],
            data["timestamp"],
            data["transactions"],
            data["creator_address"],
            data["signature"]
        )


def create_genesis_block():
    return Block(
        index=0,
        previous_hash="0",
        timestamp=int(time.time()),
        transactions=[],
        creator_address="GENESIS",
        signature="GENESIS_SIGNATURE"
    )
