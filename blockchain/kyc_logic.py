# blockchain/kyc.py

class KYCRegistry:
    def __init__(self):
        self.verified_users = set()

    def verify_user(self, email):
        self.verified_users.add(email)

    def is_verified(self, email):
        return email in self.verified_users


# كائن ثابت لاستخدامه في الراوتر
kyc_registry = KYCRegistry()


def process_kyc_document(email, document_path, selfie_path):
    """
    إجراء تحقق وهمي للوثائق - يعتبر دائماً ناجح.
    """
    kyc_registry.verify_user(email)
    return True


def is_user_verified(email):
    return kyc_registry.is_verified(email)
