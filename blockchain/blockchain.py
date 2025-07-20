from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# مسار ملف التخزين
CHAIN_FILE = os.path.join("data", "transactions.json")

# تحميل البلوكتشين من الملف
def load_blockchain():
    if not os.path.exists(CHAIN_FILE):
        return []
    with open(CHAIN_FILE, "r") as f:
        return json.load(f)

# حفظ بلوك جديد في الملف
def save_block(block):
    chain = load_blockchain()
    chain.append(block)
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

@app.route('/')
def index():
    return "1Ummah Blockchain API running successfully ✅"

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
