
📄 1Ummah Blockchain – Protocol Specification

Overview:
1Ummah is a decentralized, independent blockchain protocol designed to reward meaningful Islamic and social activity. It uses a hybrid mechanism combining Proof of Stake (PoS) and Proof of Activity (PoA), offering secure, fair, and efficient coin distribution and governance without reliance on any external blockchain.


---

🔐 Total Supply and Distribution:

Total Supply: 500,000,000 UMH (1Ummah Coin)

Community Allocation: 75% (375,000,000 UMH)

Team & Development Fund: 20% (100,000,000 UMH)

Reserve & Grants: 5% (25,000,000 UMH)



---

⚙️ Mining Mechanism:

Reward per mining cycle: 3 UMH

Cycle Duration: 24 hours

Eligibility: One cycle per user per 24 hours

Referrals: A 2% bonus starting from the 30th mining cycle of the referred user

Referral payout is accumulated and transferred automatically after cycle 30



---

👤 KYC System:

Verification Required: For mining, sending, and receiving

Methods: Document upload + facial recognition

Restriction: Only KYC-verified users can transfer or receive funds



---

💸 Transactions:

Minimum Transfer Amount: 21 UMH

Daily Limit: 1 transaction per user per day

Only KYC-approved users can initiate or receive transactions

Transactions are validated within the internal block confirmation logic



---

🔏 Wallet System:

Encrypted Wallets: With 12-word mnemonic recovery phrase

Multiple Wallets per User: Allowed

Random address generation per wallet

Each wallet maintains its own balance and transaction history



---

🧠 Smart Logic (Embedded in Blockchain):

Issuance: Only by admin key

Burn: Can only be triggered by admin

Consensus: Custom hybrid of PoS and PoA

Block validation includes:

Time restrictions

KYC enforcement

Referral logic

Signature verification




---

🛡️ Security Features:

Multi-layer encryption

Replay attack protection

51% attack mitigation by using stake+activity combination

Tamper detection within each block hash



---

💻 Developer Notes:

All logic is written in Python and split across modular files for easy auditing.

No third-party blockchain dependency (not based on Ethereum or any public chain).

Fully open-source and documented on GitHub.

