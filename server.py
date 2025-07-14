from flask import Flask, request, jsonify
from blockchain.wallet import Wallet
from blockchain.kyc import KYCRegistry
from blockchain.chain import Blockchain
from blockchain.admin import issue_coins, burn_coins

app = Flask(__name__)

# النظام الأساسي
blockchain = Blockchain()
kyc = KYCRegistry()

@app.route("/")
def index():
    return "1Ummah Blockchain API is running."

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")

    # إنشاء محفظة جديدة
    wallet = Wallet()
    address = wallet.get_address()

    # حفظ المحفظة في قاعدة البيانات أو ملف مؤقت (غير مفعّل حالياً)
    return jsonify({
        "message": "User registered successfully.",
        "email": email,
        "wallet": wallet.to_dict()
    })

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    # تسجيل الدخول (هذا مجرد مثال ثابت)
    return jsonify({
        "message": f"Welcome back, {email}!"
    })

if __name__ == "__main__":
    app.run(debug=True)
