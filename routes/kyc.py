# routes/kyc.py

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from blockchain.kyc_logic import process_kyc_document, is_user_verified

kyc_bp = Blueprint("kyc_bp", __name__)

UPLOAD_FOLDER = 'uploads/kyc_documents'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@kyc_bp.route('/upload_kyc', methods=['POST'])
def upload_kyc():
    user_id = request.form.get('user_id')
    file = request.files.get('file')

    if not user_id or not file or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid input'}), 400

    filename = secure_filename(f"{user_id}_{file.filename}")
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    result = process_kyc_document(user_id, save_path)
    return jsonify({'result': result})

@kyc_bp.route('/kyc_status/<user_id>', methods=['GET'])
def kyc_status(user_id):
    status = is_user_verified(user_id)
    return jsonify({'kyc_verified': status})
