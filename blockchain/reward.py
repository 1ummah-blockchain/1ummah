# blockchain/reward.py



import time

from .transaction import Transaction

from .config import DAILY_REWARD





# التحقق إن المستخدم له الحق في التعدين اليومي

def is_eligible_for_reward(last_mining_time):

    now = int(time.time())

    return now - last_mining_time >= 86400  # 24 ساعة





# توليد معاملة المكافأة اليومية

def get_daily_reward_transaction(miner_address):

    return Transaction(

        sender="COINBASE",

        recipient=miner_address,

        amount=DAILY_REWARD

    )
