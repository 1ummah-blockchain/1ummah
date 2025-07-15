# blockchain/kyc.py

class KYCRegistry:
    def __init__(self):
        self.verified_users = set()

    def verify_user(self, address_or_email):
        self.verified_users.add(address_or_email)

    def is_verified(self, address_or_email):
        return address_or_email in self.verified_users


# سجل واحد مشترك
kyc_registry = KYCRegistry()


def process_kyc_document(email, document_path, selfie_path):
    """
    محاكاة عملية تحقق KYC ناجحة.
    """
    kyc_registry.verify_user(email)
    return True


def is_user_verified(email):
    return kyc_registry.is_verified(email)
