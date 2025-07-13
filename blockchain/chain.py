# blockchain/chain.py



import time

from .block import Block, create_genesis_block

from .transaction import Transaction

from .config import BLOCK_TIME_SECONDS, ADMIN_ADDRESS, TOTAL_SUPPLY

from .reward import is_eligible_for_reward, get_daily_reward_transaction

from .referral import get_referral_bonus_transaction





class Blockchain:

    def __init__(self):

        self.chain = [create_genesis_block()]

        self.pending_transactions = []

        self.balances = {ADMIN_ADDRESS: TOTAL_SUPPLY}

        self.last_mining_times = {}



    def get_last_block(self):

        return self.chain[-1]



    def add_transaction(self, tx):

        if tx.is_valid():

            self.pending_transactions.append(tx)

            return True

        return False



    def get_balance(self, address):

        return self.balances.get(address, 0)



    def is_valid_chain(self):

        for i in range(1, len(self.chain)):

            current = self.chain[i]

            previous = self.chain[i - 1]

            if current.previous_hash != previous.hash:

                return False

            if current.hash != current.calculate_hash():

                return False

        return True



    def mine_pending_transactions(self, miner_address, cycle_count, referrer=None):

        now = int(time.time())

        last_mined = self.last_mining_times.get(miner_address, 0)



        if now - last_mined < BLOCK_TIME_SECONDS:

            return None  # لم يمر وقت كافي للتعدين



        reward_tx = get_daily_reward_transaction(miner_address)

        transactions = [reward_tx]



        if referrer and cycle_count >= 30:

            ref_tx = get_referral_bonus_transaction(referrer, miner_address)

            if ref_tx:

                transactions.append(ref_tx)



        transactions.extend(self.pending_transactions)



        new_block = Block(

            index=len(self.chain),

            previous_hash=self.get_last_block().hash,

            timestamp=now,

            transactions=[tx.to_dict() for tx in transactions],

            creator_address=miner_address

        )

        self.chain.append(new_block)



        for tx in transactions:

            self._update_balances(tx)



        self.pending_transactions = []

        self.last_mining_times[miner_address] = now



        return new_block



    def _update_balances(self, tx):

        sender = tx["sender"]

        recipient = tx["recipient"]

        amount = tx["amount"]



        if sender != "COINBASE":

            self.balances[sender] = self.balances.get(sender, 0) - amount



        self.balances[recipient] = self.balances.get(recipient, 0) + amount
