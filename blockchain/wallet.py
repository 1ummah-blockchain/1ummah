# blockchain/wallet.py

import base58
from ecdsa import SigningKey, SECP256k1
from .crypto_utils import sign_message, verify_signature, serialize_public_key

class Wallet:
    def __init__(self, private_key=None):
        if private_key:
            self.signing_key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        else:
            self.signing_key = SigningKey.generate(curve=SECP256k1)

        self.verifying_key = self.signing_key.verifying_key
        self.address = self.generate_address()

    def generate_address(self):
        pub_key_bytes = self.verifying_key.to_string()
        address_bytes = base58.b58encode(pub_key_bytes)
        return address_bytes.decode()

    def get_private_key(self):
        return self.signing_key.to_string().hex()

    def get_public_key(self):
        return serialize_public_key(self.verifying_key)

    def sign(self, message):
        return sign_message(self.signing_key, message)

    def verify(self, message, signature):
        return verify_signature(self.verifying_key, message, signature)
