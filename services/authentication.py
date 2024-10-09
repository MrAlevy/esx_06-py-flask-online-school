"""
This module provides functions for hashing and verifying passwords using bcrypt.
"""

import bcrypt


def hash_password(password):
    """
    Hash a plaintext password using bcrypt.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password, password_hash):
    """
    Verify a plaintext password against the hashed password.
    """
    return bcrypt.checkpw(password.encode("utf-8"), password_hash)
