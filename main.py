import json
import os
from datetime import datetime, timedelta

DATA_FILE = "data.json"
REWARD_PER_MINING = 3
MINING_INTERVAL_HOURS = 24

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def create_user(data, address):
    if address in data["users"]:
        return
    data["users"][address] = {
        "balance": 0,
        "last_mining_time": None,
        "kyc_verified": False,
        "referrer": None,
        "mining_cycles": 0,
        "referral_bonus_collected": False,
        "referrals_count": 0,
        "account_status": "active",
        "username": "",
        "rank": "bronze",
        "points": 0,
        "verified_badge": False,
        "avatar_url": "",
        "transactions": []
    }

def can_mine(last_time):
    if not last_time:
        return True
    last = datetime.fromisoformat(last_time)
    return datetime.utcnow() - last >= timedelta(hours=MINING_INTERVAL_HOURS)

def mine(data, address):
    user = data["users"][address]
    if can_mine(user["last_mining_time"]):
        user["balance"] += REWARD_PER_MINING
        user["last_mining_time"] = datetime.utcnow().isoformat()
        user["mining_cycles"] += 1
        user["transactions"].append({
            "type": "mine",
            "amount": REWARD_PER_MINING,
            "timestamp": user["last_mining_time"]
        })
        print(f"✅ Mined {REWARD_PER_MINING} UMH successfully.")
    else:
        print("⏳ Please wait before mining again.")

def show_user_info(data, address):
    user = data["users"][address]
    print(f"\n📌 Address: {address}")
    print(f"🪙 Balance: {user['balance']} UMH")
    print(f"🔁 Mining cycles: {user['mining_cycles']}")
    print(f"🔐 KYC Verified: {'✅' if user['kyc_verified'] else '❌'}")
    print(f"🏅 Rank: {user['rank']}")
    print(f"📛 Username: {user['username'] or 'N/A'}")
    print(f"🧲 Referrals: {user['referrals_count']}")
    print()

def main():
    address = input("🔑 Enter your wallet address: ").strip()
    data = load_data()
    create_user(data, address)

    while True:
        print("\n📋 Menu:")
        print("1. Mine")
        print("2. Show account info")
        print("3. Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            mine(data, address)
        elif choice == "2":
            show_user_info(data, address)
        elif choice == "3":
            save_data(data)
            print("🔒 Data saved. Exiting.")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
