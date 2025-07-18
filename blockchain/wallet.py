import os
import random
import hashlib
import base58
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import randrange_from_seed__trytryagain

class Wallet:
    def __init__(self, private_key=None):
        if private_key:
            self.signing_key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        else:
            self.signing_key = SigningKey.generate(curve=SECP256k1)

        self.verifying_key = self.signing_key.verifying_key
        self.private_key = self.signing_key.to_string().hex()
        self.public_key = self.serialize_public_key(self.verifying_key)
        self.address = self.generate_address(self.public_key)
        self.recovery_phrase = self.generate_recovery_phrase()

    def serialize_public_key(self, verifying_key):
        return verifying_key.to_string().hex()

    def generate_address(self, public_key_hex):
        sha256_hash = hashlib.sha256(bytes.fromhex(public_key_hex)).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        return base58.b58encode(ripemd160.digest()).decode()

    def generate_recovery_phrase(self):
        words = []
        for _ in range(12):
            word = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
            words.append(word)
        return ' '.join(words)

    def sign(self, message):
        return self.signing_key.sign(message.encode()).hex()

    def verify(self, message, signature_hex):
        try:
            return self.verifying_key.verify(bytes.fromhex(signature_hex), message.encode())
        except:
            return False

    def to_dict(self):
        return {
            "private_key": self.private_key,
            "public_key": self.public_key,
            "address": self.address,
            "recovery_phrase": self.recovery_phrase
        }

# دالة مساعدة لتوليد محفظة جديدة
def generate_wallet():
    wallet = Wallet()
    return wallet.to_dict()
