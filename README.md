# 1Ummah Blockchain

**1Ummah** is a fully independent, open-source blockchain project inspired by the concept of unity and collaboration within the Muslim Ummah (nation). This blockchain is designed to reward meaningful actions, support Islamic and humanitarian causes, and create a decentralized, fair, and secure digital ecosystem.

---

## 🌟 Project Vision

> “Ummah” means “One Nation.” This project empowers a decentralized system that promotes good deeds, supports community-driven growth, and reflects Islamic values of fairness, transparency, and trust.

---

## 🪙 Token Specifications

| Property             | Value                      |
|----------------------|----------------------------|
| Name                 | 1Ummah                     |
| Symbol               | UMH                        |
| Total Supply         | 1,000,000,000 UMH (Fixed)  |
| Mining Reward        | 3 UMH per cycle (once every 24h) |
| Validators           | Users with ≥ 2 UMH         |
| Referral Bonus       | 2% after 30 mining cycles  |
| Burn Mechanism       | 2% burned on every transfer |
| Blockchain           | Fully independent (not Ethereum or BSC) |
| KYC Required         | Yes (before mining or sending tokens) |

---

## 🔐 Security Features

- ECDSA Digital Signatures on every block
- Full blockchain validation logic
- User-specific encrypted wallets
- KYC verification before transaction activity
- Separation between user roles (admin, miner, validator)

---

## 💻 Folder Structure

```
1ummah Blockchain/
│
├── blockchain/
│   ├── crypto_utils.py     # Digital signatures and key generation
│   ├── user.py             # User accounts, wallets, KYC
│   ├── block.py            # Block definition and hashing
│   └── blockchain.py       # Core blockchain logic: mining, transfer, staking, validation
│
├── data/                   # Persistent storage for users and blocks
│
├── README.md               # Project overview
└── requirements.txt        # Python dependencies
```

---

## 🚀 Getting Started

1. **Install Python 3.8+**
2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Import the blockchain engine and start coding**

```python
from blockchain.blockchain import Blockchain

bc = Blockchain()
bc.user_manager.register_user("user1")
bc.user_manager.update_kyc("user1", True, {"doc_type": "Passport", "id": "123456"})
bc.mine("user1")
```

---

## 🔁 Key Functionalities

- **Proof of Activity**: Users mine UMH tokens by participating in daily tasks.
- **Proof of Stake**: Validators must hold ≥ 2 UMH to sign blocks.
- **Referral System**: Referrer earns 2% of reward after 30 mining cycles.
- **KYC Enforcement**: No mining or transfers without verification.
- **Token Burn**: 2% of transferred amount is burned forever.

---

## 📄 License

This project is 100% open source and welcomes contributions from developers around the world. All work must respect the project's values: transparency, security, fairness, and social good.

---

## 🤝 Contributing

We welcome developers from all backgrounds to contribute!  
Open a pull request, suggest a new feature, or help us fix bugs.  
Together we build something impactful for the Ummah and the world.
