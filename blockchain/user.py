import json

import os

from typing import Optional

from .crypto_utils import generate_keys, serialize_public_key, deserialize_public_key



DATA_FILE = 'data/users_data.json'



class User:

    def __init__(self, address: str, private_key=None, public_key=None):

        self.address = address  # عنوان المستخدم (محفظته)

        if private_key and public_key:

            self.private_key = private_key

            self.public_key = public_key

        else:

            self.private_key, self.public_key = generate_keys()

        self.public_key_str = serialize_public_key(self.public_key)

        self.balance = 0.0

        self.mining_cycles = 0

        self.last_mining_timestamp = 0

        self.referral_paid = False

        self.referrer: Optional[str] = None

        self.kyc_verified = False

        self.kyc_documents = {}  # حفظ مستندات KYC كـ {نوع: بيانات}



    def to_dict(self):

        return {

            'address': self.address,

            'public_key': self.public_key_str,

            'balance': self.balance,

            'mining_cycles': self.mining_cycles,

            'last_mining_timestamp': self.last_mining_timestamp,

            'referral_paid': self.referral_paid,

            'referrer': self.referrer,

            'kyc_verified': self.kyc_verified,

            'kyc_documents': self.kyc_documents

        }



    @staticmethod

    def from_dict(data):

        user = User(data['address'])

        user.public_key_str = data['public_key']

        user.public_key = deserialize_public_key(user.public_key_str)

        user.balance = data.get('balance', 0.0)

        user.mining_cycles = data.get('mining_cycles', 0)

        user.last_mining_timestamp = data.get('last_mining_timestamp', 0)

        user.referral_paid = data.get('referral_paid', False)

        user.referrer = data.get('referrer', None)

        user.kyc_verified = data.get('kyc_verified', False)

        user.kyc_documents = data.get('kyc_documents', {})

        return user



class UserManager:

    def __init__(self):

        self.users = {}

        self.load_users()



    def load_users(self):

        if os.path.exists(DATA_FILE):

            with open(DATA_FILE, 'r') as f:

                data = json.load(f)

                for addr, udata in data.items():

                    self.users[addr] = User.from_dict(udata)



    def save_users(self):

        data = {addr: user.to_dict() for addr, user in self.users.items()}

        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

        with open(DATA_FILE, 'w') as f:

            json.dump(data, f, indent=4)



    def register_user(self, address: str, referrer: Optional[str] = None) -> bool:

        if address in self.users:

            print("المستخدم مسجل سابقًا.")

            return False

        user = User(address)

        if referrer and referrer in self.users and referrer != address:

            user.referrer = referrer

        self.users[address] = user

        self.save_users()

        print(f"تم تسجيل المستخدم {address} بنجاح.")

        return True



    def get_user(self, address: str) -> Optional[User]:

        return self.users.get(address)



    def update_kyc(self, address: str, verified: bool, documents: dict):

        user = self.get_user(address)

        if not user:

            print("المستخدم غير موجود.")

            return False

        user.kyc_verified = verified

        user.kyc_documents = documents

        self.save_users()

        print(f"KYC للمستخدم {address} تم تحديثه.")

        return True
