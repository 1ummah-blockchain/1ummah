# blockchain/chain.py

import time
import hashlib
from .block import Block
from .transaction import Transaction

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.users = {}  # قاعدة بيانات مؤقتة للمستخدمين
        self.load_genesis_block()

    def load_genesis_block(self):
        if not self.chain:
            genesis_block = Block(0, "0", [], time.time())
            self.chain.append(genesis_block)

    def add_transaction(self, transaction: Transaction):
        is_valid, message = Transaction.is_valid(transaction, self.users)

        if not is_valid:
            return False, message

        sender = transaction.sender
        recipient = transaction.recipient
        amount = transaction.amount

        # خصم وإضافة الأرصدة
        self.users[sender]["balance"] -= amount
        self.users[recipient]["balance"] += amount

        self.pending_transactions.append(transaction)
        return True, "Transaction added successfully"

    def mine_block(self, miner_address):
        if not self.pending_transactions:
            return False, "No transactions to mine"

        if miner_address not in self.users or not self.users[miner_address]["kyc_passed"]:
            return False, "Miner must be a verified user"

        # مكافأة التعدين
        reward_amount = 3
        self.users[miner_address]["balance"] += reward_amount

        last_block = self.chain[-1]
        new_block = Block(
            index=last_block.index + 1,
            previous_hash=last_block.hash,
            transactions=self.pending_transactions.copy(),
            timestamp=time.time()
        )

        new_block.hash = new_block.compute_hash()
        self.chain.append(new_block)
        self.pending_transactions = []
        return True, "Block mined and added to the chain"

    def get_balance(self, address):
        user = self.users.get(address)
        if not user:
            return 0
        return user.get("balance", 0)

    def register_user(self, address):
        if address not in self.users:
            self.users[address] = {
                "balance": 0,
                "kyc_passed": False,
                "referrals": 0,
                "rank": "member"
            }

    def verify_kyc(self, address):
        if address in self.users:
            self.users[address]["kyc_passed"] = True
