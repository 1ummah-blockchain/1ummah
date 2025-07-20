from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# استيراد الراوترات
from routes.kyc import kyc_bp
from routes.mine import mine_routes  # تم تعديل هذا السطر
from routes.send import send_bp
from routes.auth import auth_bp
from routes.referral import referral_bp
from routes.wallet import wallet_bp

# إعداد التطبيق
app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# تسجيل الـ Blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(kyc_bp, url_prefix='/api')
app.register_blueprint(mine_routes, url_prefix='/api')  # تم تعديل هذا السطر
app.register_blueprint(send_bp, url_prefix='/api')
app.register_blueprint(referral_bp, url_prefix='/api')
app.register_blueprint(wallet_bp, url_prefix='/api')

# الراوت الرئيسي لواجهة المستخدم
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# راوت لدعم جميع ملفات الواجهة frontend
@app.route('/<path:path>')
def serve_static_file(path):
    return send_from_directory(app.static_folder, path)

# تشغيل التطبيق على المنفذ الصحيح لـ Cloud Run
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
