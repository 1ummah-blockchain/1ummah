import json
import os
import time

USERS_FILE = "data/users.json"

class User:
    def __init__(self, address, balance=0, kyc_verified=False, referrer=None, mining_cycles=0, referral_paid=False, last_mining_timestamp=0):
        self.address = address
        self.balance = balance
        self.kyc_verified = kyc_verified
        self.referrer = referrer
        self.mining_cycles = mining_cycles
        self.referral_paid = referral_paid
        self.last_mining_timestamp = last_mining_timestamp

    def to_dict(self):
        return {
            "address": self.address,
            "balance": self.balance,
            "kyc_verified": self.kyc_verified,
            "referrer": self.referrer,
            "mining_cycles": self.mining_cycles,
            "referral_paid": self.referral_paid,
            "last_mining_timestamp": self.last_mining_timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            address=data["address"],
            balance=data.get("balance", 0),
            kyc_verified=data.get("kyc_verified", False),
            referrer=data.get("referrer"),
            mining_cycles=data.get("mining_cycles", 0),
            referral_paid=data.get("referral_paid", False),
            last_mining_timestamp=data.get("last_mining_timestamp", 0)
        )

class UserManager:
    def __init__(self, users_file=USERS_FILE):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists(self.users_file):
            return {}
        with open(self.users_file, "r") as f:
            data = json.load(f)
            return {addr: User.from_dict(info) for addr, info in data.items()}

    def save_users(self):
        with open(self.users_file, "w") as f:
            json.dump({addr: user.to_dict() for addr, user in self.users.items()}, f, indent=2)

    def get_user(self, address):
        return self.users.get(address)

    def add_user(self, user: User):
        if user.address in self.users:
            return False  # المستخدم موجود بالفعل
        self.users[user.address] = user
        self.save_users()
        return True

    def update_user(self, user: User):
        self.users[user.address] = user
        self.save_users()
