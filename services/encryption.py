"""
Service for encrypting and decrypting sensitive data.
"""

import os
from cryptography.fernet import Fernet


class EncryptionService:
    """
    Service for encrypting and decrypting sensitive data using AES-128 encryption.
    """

    def __init__(self):
        # Use a consistent key for encryption/decryption
        key = os.getenv("ENCRYPTION_KEY")
        if not key:
            # Generate a new key and set it as an environment variable
            key = Fernet.generate_key()
            os.environ["ENCRYPTION_KEY"] = key.decode()
        else:
            key = key.encode()
        self.fernet = Fernet(key)

    def encrypt(self, data):
        """
        Encrypt the data.
        """
        if isinstance(data, str):
            data = data.encode()
        return self.fernet.encrypt(data).decode()

    def decrypt(self, token):
        """
        Decrypt the data.
        """
        return self.fernet.decrypt(token.encode()).decode()
