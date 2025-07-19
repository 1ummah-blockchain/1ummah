from cryptography.fernet import Fernet

def load_key():
    with open("key.key", "rb") as key_file:
        return key_file.read()

def encrypt_data(data: str) -> str:
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data.encode()).decode()
