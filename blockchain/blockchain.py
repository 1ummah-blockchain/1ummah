from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

app = Flask(__name__)

# تهيئة Firebase
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# المجلد أو المسار الخاص بالبلوكشين في Firestore
blockchain_ref = db.collection("blockchain")

# دالة لتحميل البيانات من Firestore
def load_blockchain():
    docs = blockchain_ref.order_by("index").stream()
    return [doc.to_dict() for doc in docs]

# دالة لحفظ بلوك جديد
def save_block(block):
    blockchain_ref.document(str(block['index'])).set(block)

@app.route('/')
def index():
    return "1Ummah Blockchain API running successfully with Firestore ✅"

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    blockchain = load_blockchain()
    return jsonify(blockchain)

@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.json
    blockchain = load_blockchain()
    
    last_block = blockchain[-1] if blockchain else {"index": 0, "hash": "0"}
    new_block = {
        "index": last_block['index'] + 1,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data['data'],
        "previous_hash": last_block['hash'],
        "hash": str(hash(str(data['data']) + last_block['hash']))
    }
    save_block(new_block)
    return jsonify(new_block), 201
