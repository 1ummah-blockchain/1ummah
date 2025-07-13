# blockchain/referral.py



from .transaction import Transaction

from .config import REFERRAL_BONUS_PERCENT





# توليد معاملة مكافأة الإحالة

def get_referral_bonus_transaction(referrer_address, miner_address, amount=3):

    bonus = int(amount * REFERRAL_BONUS_PERCENT)

    if not referrer_address or referrer_address == miner_address:

        return None



    return Transaction(

        sender="COINBASE",

        recipient=referrer_address,

        amount=bonus

    )
