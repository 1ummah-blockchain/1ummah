import time
from .firestore_db import firestore

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
    def __init__(self):
        self.collection = firestore.collection("users")
        self.users = {}
        self.load_users()

    def load_users(self):
        self.users = {}
        docs = self.collection.stream()
        for doc in docs:
            user = User.from_dict(doc.to_dict())
            self.users[user.address] = user

    def save_user(self, user: User):
        self.collection.document(user.address).set(user.to_dict())
        self.users[user.address] = user

    def get_user(self, address):
        return self.users.get(address)

    def add_user(self, user: User):
        self.save_user(user)
