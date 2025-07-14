from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# إعدادات المسارات
UPLOAD_FOLDER = 'blockchain/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# التحقق من الامتدادات المسموح بها
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# نقطة رفع بيانات KYC
@app.route('/kyc/upload', methods=['POST'])
def upload_kyc():
    if 'id_document' not in request.files or 'face_photo' not in request.files:
        return jsonify({'error': 'Both ID document and face photo are required'}), 400

    id_file = request.files['id_document']
    face_file = request.files['face_photo']
    user_id = request.form.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    if id_file and allowed_file(id_file.filename) and face_file and allowed_file(face_file.filename):
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_id))
        os.makedirs(user_folder, exist_ok=True)

        id_path = os.path.join(user_folder, secure_filename('id_' + id_file.filename))
        face_path = os.path.join(user_folder, secure_filename('face_' + face_file.filename))

        id_file.save(id_path)
        face_file.save(face_path)

        return jsonify({'message': 'KYC documents uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
