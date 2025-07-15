# blockchain/kyc.py

class KYCRegistry:
    def __init__(self):
        self.verified_users = set()

    def verify_user(self, address):
        self.verified_users.add(address)

    def is_verified(self, address):
        return address in self.verified_users


# كائن مشترك يُستخدم داخل دوال أخرى
registry = KYCRegistry()


def process_kyc_document(email, document_path, selfie_path):
    # معالجة وهمية – نعتبر أن التحقق ناجح
    registry.verify_user(email)
    return True


def is_user_verified(email):
    return registry.is_verified(email)
