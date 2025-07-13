# blockchain/wallet.py



from ecdsa import SigningKey, VerifyingKey, SECP256k1

import hashlib

import os

import json

import base64

from .crypto_utils import sign_message, verify_signature, serialize_public_key





class Wallet:

    def __init__(self, private_key=None):

        if private_key:

            self.private_key = SigningKey.from_string(

                bytes.fromhex(private_key), curve=SECP256k1)

        else:

            self.private_key = SigningKey.generate(curve=SECP256k1)



        self.public_key = self.private_key.get_verifying_key()



    def get_private_key(self):

        return self.private_key.to_string().hex()



    def get_public_key(self):

        return serialize_public_key(self.public_key)



    def get_address(self):

        pub_key_bytes = self.public_key.to_string()

        address = hashlib.sha256(pub_key_bytes).hexdigest()

        return address



    def sign(self, message):

        return sign_message(self.private_key, message)



    def to_dict(self):

        return {

            "private_key": self.get_private_key(),

            "public_key": self.get_public_key(),

            "address": self.get_address()

        }



    @staticmethod

    def from_dict(data):

        return Wallet(private_key=data["private_key"])
