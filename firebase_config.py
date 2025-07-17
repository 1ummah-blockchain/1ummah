import firebase_admin
from firebase_admin import credentials, firestore

# تحميل بيانات الحساب من المسار الصحيح
cred = credentials.Certificate('config/serviceAccountKey.json')

# تهيئة Firebase
firebase_admin.initialize_app(cred)

# تهيئة قاعدة بيانات Firestore
db = firestore.client()
