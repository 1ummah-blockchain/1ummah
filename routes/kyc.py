from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from firestore_db import db  # تأكد أن هذا الملف موجود ويعمل بشكل سليم
from blockchain.kyc_logic import process_kyc_document, is_user_verified  # تأكد من صحة هذه الدوال

kyc_bp = Blueprint("kyc_bp", __name__)

UPLOAD_FOLDER = 'uploads/kyc_documents'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# إنشاء المجلد إذا لم يكن موجودًا
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """التحقق من أن الملف من نوع مسموح به"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@kyc_bp.route('/upload_kyc', methods=['POST'])
def upload_kyc():
    """نقطة نهاية لتحميل مستند KYC"""
    user_id = request.form.get('user_id')
    file = request.files.get('file')

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    if not file or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid or missing file'}), 400

    # تأمين اسم الملف
    filename = secure_filename(file.filename)
    user_folder = os.path.join(UPLOAD_FOLDER, user_id)
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, filename)

    # حفظ الملف في المسار المطلوب
    file.save(file_path)

    # استدعاء منطق التحقق من الوثيقة
    try:
        verification_result = process_kyc_document(user_id, file_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'result': verification_result}), 200

@kyc_bp.route('/kyc_status/<user_id>', methods=['GET'])
def kyc_status(user_id):
    """التحقق من حالة المستخدم إذا تم التحقق منه"""
    try:
        status = is_user_verified(user_id)
        return jsonify({'kyc_verified': status}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
