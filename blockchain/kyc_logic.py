# blockchain/kyc_logic.py

import json
import os

KYC_DATA_FILE = "data/kyc_users.json"
os.makedirs("data", exist_ok=True)

# تحميل بيانات KYC من الملف
def load_kyc_data():
    if not os.path.exists(KYC_DATA_FILE):
        return {}
    with open(KYC_DATA_FILE, "r") as f:
        return json.load(f)

# حفظ بيانات KYC إلى الملف
def save_kyc_data(data):
    with open(KYC_DATA_FILE, "w") as f:
        json.dump(data, f)

class KYCRegistry:
    def __init__(self):
        self.kyc_users = load_kyc_data()

    def verify_user(self, user_id):
        self.kyc_users[user_id] = True
        save_kyc_data(self.kyc_users)

    def is_verified(self, user_id):
        return self.kyc_users.get(user_id, False)

# كائن ثابت للاستخدام
kyc_registry = KYCRegistry()

def process_kyc_document(user_id, document_path):
    # تحقق وهمي – دائمًا ناجح
    kyc_registry.verify_user(user_id)
    return True

def is_user_verified(user_id):
    return kyc_registry.is_verified(user_id)
