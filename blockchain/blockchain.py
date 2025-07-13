import os
import json
import time
from .block import Block
from .user import UserManager
from .crypto_utils import verify_signature

BLOCKCHAIN_DATA_FILE = 'data/blockchain_data.json'

class Blockchain:
    def __init__(self):
        self.chain = []
        self.user_manager = UserManager()
        self.load_blockchain()

    def create_genesis_block(self):
        genesis = Block(0, "0", [], "GENESIS")
        self.chain.append(genesis)
        self.save_blockchain()

    def load_blockchain(self):
        if os.path.exists(BLOCKCHAIN_DATA_FILE):
            with open(BLOCKCHAIN_DATA_FILE, 'r') as f:
                data = json.load(f)
                self.chain = [Block.from_dict(b) for b in data]
        else:
            self.create_genesis_block()

    def save_blockchain(self):
        data = [block.to_dict() for block in self.chain]
        os.makedirs(os.path.dirname(BLOCKCHAIN_DATA_FILE), exist_ok=True)
        with open(BLOCKCHAIN_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def get_last_block(self):
        return self.chain[-1]

    def select_validator(self):
        # أبسط اختيار: أول مستخدم رصيده >= 2
        for user in self.user_manager.users.values():
            if user.balance >= 2:
                return user
        return None

    def mine(self, address: str):
        user = self.user_manager.get_user(address)
        if not user:
            print("المستخدم غير مسجل.")
            return

        if not user.kyc_verified:
            print("المستخدم لم يجتز KYC.")
            return

        now = time.time()
        if now - user.last_mining_timestamp < 86400:  # 24 ساعة
            print("لا يمكن التعدين أكثر من مرة كل 24 ساعة.")
            return

        # مكافأة التعدين
        reward = 3
        user.balance += reward
        user.last_mining_timestamp = now
        user.mining_cycles += 1

        transactions = [{
            "type": "mining",
            "to": address,
            "amount": reward,
            "timestamp": now
        }]

        # تحقق من مكافأة الإحالة
        if user.referrer and not user.referral_paid and user.mining_cycles >= 30:
            ref_user = self.user_manager.get_user(user.referrer)
            if ref_user:
                referral_bonus = reward * 0.02
                ref_user.balance += referral_bonus
                transactions.append({
                    "type": "referral_bonus",
                    "to": user.referrer,
                    "from": address,
                    "amount": referral_bonus,
                    "timestamp": now
                })
                user.referral_paid = True

        # المدقق
        validator = self.select_validator()
        if not validator:
            print("لا يوجد مدقق متاح.")
            return

        block = Block(
            index=len(self.chain),
            previous_hash=self.get_last_block().hash,
            transactions=transactions,
            validator=validator.address
        )
        block.sign_block(validator.private_key)
        self.chain.append(block)
        self.save_blockchain()
        self.user_manager.save_users()
        print(f"تم تعدين بلوك #{block.index} للمستخدم {address}.")

    def transfer(self, sender_addr: str, receiver_addr: str, amount: float):
        sender = self.user_manager.get_user(sender_addr)
        receiver = self.user_manager.get_user(receiver_addr)

        if not sender or not receiver:
            print("أحد العنوانين غير مسجل.")
            return

        if not sender.kyc_verified or not receiver.kyc_verified:
            print("الطرفان يجب أن يجتازا KYC.")
            return

        if sender.balance < amount:
            print("الرصيد غير كافٍ.")
            return

        now = time.time()
        burned = amount * 0.02
        net_amount = amount - burned

        sender.balance -= amount
        receiver.balance += net_amount

        transactions = [{
            "type": "transfer",
            "from": sender_addr,
            "to": receiver_addr,
            "amount": net_amount,
            "burned": burned,
            "timestamp": now
        }]

        validator = self.select_validator()
        if not validator:
            print("لا يوجد مدقق.")
            return

        block = Block(
            index=len(self.chain),
            previous_hash=self.get_last_block().hash,
            transactions=transactions,
            validator=validator.address
        )
        block.sign_block(validator.private_key)
        self.chain.append(block)
        self.save_blockchain()
        self.user_manager.save_users()
        print(f"تم تحويل {net_amount:.2f} من {sender_addr} إلى {receiver_addr}.")

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.previous_hash != prev.hash:
                return False
            if current.hash != current.calculate_hash():
                return False
            # تحقق من التوقيع
            validator_user = self.user_manager.get_user(current.validator)
            if not validator_user or not verify_signature(validator_user.public_key, bytes.fromhex(current.signature), current.hash.encode()):
                return False
        return True
