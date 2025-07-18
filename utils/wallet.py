import os
import random
import hashlib

class Wallet:
    def __init__(self):
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key(self.private_key)
        self.address = self.generate_address(self.public_key)
        self.recovery_phrase = self.generate_recovery_phrase()

    def generate_private_key(self):
        return os.urandom(32).hex()

    def generate_public_key(self, private_key):
        return hashlib.sha256(private_key.encode()).hexdigest()

    def generate_address(self, public_key):
        return hashlib.new('ripemd160', public_key.encode()).hexdigest()

    def generate_recovery_phrase(self):
        words = []
        for _ in range(12):
            word = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
            words.append(word)
        return ' '.join(words)

    def to_dict(self):
        return {
            "private_key": self.private_key,
            "public_key": self.public_key,
            "address": self.address,
            "recovery_phrase": self.recovery_phrase
        }
