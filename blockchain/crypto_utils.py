from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

def generate_key_pair():
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

def sign_message(private_key, message):
    signature = private_key.sign(
        message.encode(),
        ec.ECDSA(hashes.SHA256())
    )
    return signature.hex()

def verify_signature(public_key, message, signature):
    try:
        public_key.verify(
            bytes.fromhex(signature),
            message.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception:
        return False

def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

def deserialize_public_key(serialized_key):
    return serialization.load_pem_public_key(
        serialized_key.encode(),
        backend=default_backend()
    )
