📄 1Ummah Blockchain – Protocol Specification

---

**Overview:**

1Ummah is a decentralized, independent blockchain protocol designed to reward meaningful Islamic and social activity. It uses a hybrid mechanism combining Proof of Stake (PoS) and Proof of Activity (PoA), offering secure, fair, and efficient coin distribution and governance without reliance on any external blockchain.

---

🔐 **Total Supply and Distribution:**

- **Total Supply:** 1,000,000,000 UMH (1Ummah Coin)

- **Community Allocation:** 75% — 750,000,000 UMH  
- **Team & Development Fund:** 20% — 200,000,000 UMH  
- **Reserve & Grants:** 5% — 50,000,000 UMH

---

⚙️ **Mining Mechanism:**

- **Reward per mining cycle:** 3 UMH  
- **Cycle Duration:** 24 hours  
- **Eligibility:** One cycle per user per 24 hours  
- **Referrals:**  
  - 2% bonus starting from the 30th mining cycle of the referred user  
  - Referral bonus is accumulated and transferred automatically every cycle after the 30th

---

👤 **KYC System:**

- **Verification Required:** For mining, sending, and receiving  
- **Methods:** Document upload + facial recognition  
- **Restriction:** Only KYC-verified users can send or receive UMH

---

💸 **Transactions:**

- **Minimum Transfer Amount:** 21 UMH  
- **Daily Limit:** One transaction per user per day  
- **Transfer Eligibility:** Both sender and receiver must be KYC-approved  
- **Transaction Validation:** Enforced within internal block logic and signature verification

---

🔏 **Wallet System:**

- **Encrypted Wallets:** Protected with 12-word mnemonic recovery phrases  
- **Multiple Wallets per User:** Allowed  
- **Wallet Address:** Randomly generated per wallet  
- **Wallet Structure:** Each wallet stores its own balance, transaction history, and keys

---

🧠 **Smart Logic (Embedded in Blockchain):**

- **Issuance:** Only possible by admin’s secure key  
- **Burning:** Only allowed by admin  
- **Consensus:** Hybrid of Proof of Stake (PoS) and Proof of Activity (PoA)  
- **Block Validation Includes:**  
  - Time enforcement  
  - KYC verification  
  - Referral logic  
  - Multi-signature and hash checks

---

🛡️ **Security Features:**

- **Multi-layer encryption**
- **Replay attack protection**
- **51% attack resistance using PoS + PoA**
- **Tamper detection in block hash**

---

💻 **Developer Notes:**

- **Language:** Entirely written in Python  
- **Structure:** Modular file system for clarity and maintenance  
- **Independence:** No reliance on Ethereum or third-party chains  
- **Status:** Fully open-source and available on GitHub
