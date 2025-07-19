from flask import Blueprint, request, jsonify
import os
import json

activity_bp = Blueprint("activity_bp", __name__)

DATA_DIR = 'data'
ACTIVITY_LOG_PATH = os.path.join(DATA_DIR, 'activity_log.json')


def ensure_data_directory():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_activity_log():
    ensure_data_directory()
    if not os.path.exists(ACTIVITY_LOG_PATH):
        with open(ACTIVITY_LOG_PATH, 'w') as f:
            json.dump({}, f)
    with open(ACTIVITY_LOG_PATH, 'r') as f:
        return json.load(f)

def save_activity_log(log):
    ensure_data_directory()
    with open(ACTIVITY_LOG_PATH, 'w') as f:
        json.dump(log, f, indent=2)


@activity_bp.route("/api/activity/proof", methods=["POST"])
def submit_activity_proof():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"success": False, "message": "Email is required."}), 400

    log = load_activity_log()
    log[email] = True  # إثبات النشاط مسجل لهذا المستخدم
    save_activity_log(log)

    return jsonify({"success": True, "message": "✅ Activity confirmed! You can now mine."}), 200
