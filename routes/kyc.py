# routes/kyc.py

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from blockchain.kyc import process_kyc_document, is_user_verified

kyc_bp = Blueprint("kyc_bp", __name__)

UPLOAD_FOLDER = 'uploads/kyc_documents'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@kyc_bp.route('/kyc/upload', methods=['POST'])
def upload_kyc():
    email = request.form.get('email', '')
    if not email:
        return jsonify({'success': False, 'message': 'Email is required.'}), 400

    if 'document' not in request.files or 'selfie' not in request.files:
        return jsonify({'success': False, 'message': 'Both document and selfie are required.'}), 400

    document = request.files['document']
    selfie = request.files['selfie']

    if document.filename == '' or selfie.filename == '':
        return jsonify({'success': False, 'message': 'Both files must have names.'}), 400

    if not allowed_file(document.filename) or not allowed_file(selfie.filename):
        return jsonify({'success': False, 'message': 'Only PNG, JPG, JPEG allowed.'}), 400

    doc_filename = secure_filename(f"{email}_doc.{document.filename.rsplit('.', 1)[1].lower()}")
    selfie_filename = secure_filename(f"{email}_selfie.{selfie.filename.rsplit('.', 1)[1].lower()}")

    document_path = os.path.join(UPLOAD_FOLDER, doc_filename)
    selfie_path = os.path.join(UPLOAD_FOLDER, selfie_filename)

    document.save(document_path)
    selfie.save(selfie_path)

    result = process_kyc_document(email, document_path, selfie_path)

    return jsonify({'success': result, 'message': 'KYC submitted successfully' if result else 'KYC failed'}), 200

@kyc_bp.route('/kyc/status/<email>', methods=['GET'])
def check_kyc_status(email):
    verified = is_user_verified(email)
    return jsonify({'email': email, 'verified': verified}), 200
