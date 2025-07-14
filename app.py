from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from routes.kyc import kyc_bp
from routes.mine import mine_bp
from routes.send import send_bp
from routes.auth import auth_bp
from routes.referral import referral_bp
from models import db
import os

app = Flask(__name__)
CORS(app)

# إعداد الاتصال بقاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///blockchain.db')  # تستخدم SQLite مؤقتًا إذا لم تتوفر قاعدة
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# تهيئة قاعدة البيانات
db.init_app(app)

# إنشاء الجداول إذا لم تكن موجودة
with app.app_context():
    db.create_all()

# تسجيل الـ Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(kyc_bp, url_prefix='/api/kyc')
app.register_blueprint(mine_bp, url_prefix='/api/mine')
app.register_blueprint(send_bp, url_prefix='/api/send')
app.register_blueprint(referral_bp, url_prefix='/api/referral')

# نقطة اختبار
@app.route('/')
def index():
    return {'message': '1Ummah Blockchain API is running.'}, 200

if __name__ == '__main__':
    app.run(debug=True)
