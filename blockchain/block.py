# blockchain/block.py

import time
import hashlib
from .transaction import Transaction

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions  # قائمة المعاملات (كائنات Transaction)
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        tx_data = [tx.to_dict() for tx in self.transactions]
        block_string = f"{self.index}{self.previous_hash}{tx_data}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash
        }
