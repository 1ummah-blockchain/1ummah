import os
import sys
from data.users import add_user
from blockchain.wallet import generate_wallet

def register_user():
    print("مرحبًا بك في تسجيل مستخدم جديد")
    username = input("أدخل اسم المستخدم: ").strip()

    wallet_data = generate_wallet()
    success = add_user(username, wallet_data)

    if success:
        print(f"تم إنشاء المستخدم '{username}' بنجاح.")
        print("عنوان المحفظة:", wallet_data["address"])
        print("كلمات الاستعادة:", ", ".join(wallet_data["recovery_phrase"].split()))
    else:
        print(f"المستخدم '{username}' موجود بالفعل.")

if __name__ == "__main__":
    register_user()
