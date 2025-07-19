import os
import sys
from argon2 import PasswordHasher
from data.users import add_user
from blockchain.wallet import generate_wallet

# إنشاء كائن للتشفير
ph = PasswordHasher()

def register_user():
    print("مرحبًا بك في تسجيل مستخدم جديد")
    username = input("أدخل اسم المستخدم: ").strip()
    password = input("أدخل كلمة المرور: ").strip()

    # تشفير كلمة المرور
    hashed_password = ph.hash(password)

    # توليد المحفظة
    wallet_data = generate_wallet()
    wallet_data["password"] = hashed_password  # نضيف كلمة المرور المشفّرة ضمن بيانات المستخدم

    # إرسال البيانات إلى دالة الإضافة
    success = add_user(username, wallet_data)

    if success:
        print(f"تم إنشاء المستخدم '{username}' بنجاح.")
        print("عنوان المحفظة:", wallet_data["address"])
        print("كلمات الاستعادة:", ", ".join(wallet_data["recovery_phrase"].split()))
    else:
        print(f"المستخدم '{username}' موجود بالفعل.")

if __name__ == "__main__":
    register_user()
