# blockchain/kyc_logic.py

from firestore_db import db  # تأكد أن هذا الملف يحتوي على تهيئة Firestore بشكل صحيح

class KYCRegistry:
    def verify_user(self, email):
        """
        تخزين حالة التحقق في Firestore داخل مجموعة kyc_users
        """
        db.collection('kyc_users').document(email).set({'verified': True})

    def is_verified(self, email):
        """
        التحقق من حالة المستخدم من قاعدة بيانات Firestore
        """
        doc = db.collection('kyc_users').document(email).get()
        return doc.exists and doc.to_dict().get('verified', False)

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
