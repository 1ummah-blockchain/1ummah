# blockchain/crypto_utils.py



from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError

import base64





def sign_message(private_key, message):

    if isinstance(message, str):

        message = message.encode()

    signature = private_key.sign(message)

    return base64.b64encode(signature).decode()





def verify_signature(public_key_hex, message, signature):

    try:

        public_key_bytes = bytes.fromhex(public_key_hex)

        verifying_key = VerifyingKey.from_string(public_key_bytes, curve=SECP256k1)

        if isinstance(message, str):

            message = message.encode()

        decoded_signature = base64.b64decode(signature)

        return verifying_key.verify(decoded_signature, message)

    except (BadSignatureError, Exception):

        return False





def serialize_public_key(public_key):

    return public_key.to_string().hex()
