# blockchain/admin.py



from .transaction import Transaction

from .config import ADMIN_ADDRESS





def is_admin(address):

    return address == ADMIN_ADDRESS





# إنشاء معاملة إصدار جديدة من طرف المدير

def issue_coins(to_address, amount, caller):

    if not is_admin(caller):

        raise PermissionError("Unauthorized: Only admin can issue coins.")



    return Transaction(

        sender="COINBASE",

        recipient=to_address,

        amount=amount

    )





# إنشاء معاملة حرق (تدمير) العملات

def burn_coins(from_address, amount, caller):

    if not is_admin(caller):

        raise PermissionError("Unauthorized: Only admin can burn coins.")



    return Transaction(

        sender=from_address,

        recipient="BURN_ADDRESS",

        amount=amount

    )
