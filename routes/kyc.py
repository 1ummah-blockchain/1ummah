# routes/kyc.py

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from blockchain.kyc import process_kyc_document, is_user_verified

kyc_routes = Blueprint('kyc_routes', __name__)

UPLOAD_FOLDER = 'uploads/kyc_documents'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# تأكد من وجود مجلد الرفع
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@kyc_routes.route('/kyc/upload', methods=['POST'])
def upload_kyc():
    email = request.form.get('email', '')
    if 'document' not in request.files or 'selfie' not in request.files:
        return jsonify({'success': False, 'message': 'Both document and selfie are required.'}), 400

    document = request.files['document']
    selfie = request.files['selfie']

    if document.filename == '' or selfie.filename == '':
        return jsonify({'success': False, 'message': 'Files must have a name.'}), 400

    if not allowed_file(document.filename) or not allowed_file(selfie.filename):
        return jsonify({'success': False, 'message': 'Only PNG, JPG, JPEG allowed.'}), 400

    doc_filename = secure_filename(f"{email}_doc.{document.filename.rsplit('.', 1)[1].lower()}")
    selfie_filename = secure_filename(f"{email}_selfie.{selfie.filename.rsplit('.', 1)[1].lower()}")

    document_path = os.path.join(UPLOAD_FOLDER, doc_filename)
    selfie_path = os.path.join(UPLOAD_FOLDER, selfie_filename)

    document.save(document_path)
    selfie.save(selfie_path)

    # استخدم الكود من blockchain.kyc لمعالجة الوثائق
    result = process_kyc_document(email=email, document_path=document_path, selfie_path=selfie_path)

    return jsonify({'success': result, 'message': 'KYC submitted successfully' if result else 'KYC failed'}), 200

@kyc_routes.route('/kyc/status/<email>', methods=['GET'])
def check_kyc_status(email):
    status = is_user_verified(email)
    return jsonify({'email': email, 'verified': status}), 200
