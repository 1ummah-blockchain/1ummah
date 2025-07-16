import firebase_admin
from firebase_admin import credentials, firestore
import os

# تحميل بيانات الاعتماد من المتغير البيئي
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# إنشاء كائن لقاعدة البيانات
db = firestore.client()
