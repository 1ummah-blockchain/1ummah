import os
import tempfile
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

kyc_bp = Blueprint('kyc', __name__)

# ❗ استخدم مجلد مؤقت آمن في /tmp
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'kyc_uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# أنشئ المجلد لو مش موجود
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@kyc_bp.route('/upload_kyc', methods=['POST'])
def upload_kyc():
    if 'file' not in request.files or 'user_id' not in request.form:
        return jsonify({'error': 'Missing file or user ID'}), 400

    file = request.files['file']
    user_id = request.form['user_id']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(user_id + "_" + file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return jsonify({'message': 'KYC uploaded successfully', 'file_path': file_path}), 200

    return jsonify({'error': 'File type not allowed'}), 400
