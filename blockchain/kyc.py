# blockchain/kyc.py



class KYCRegistry:

    def __init__(self):

        self.verified_users = set()



    def verify_user(self, address):

        self.verified_users.add(address)



    def is_verified(self, address):

        return address in self.verified_users
