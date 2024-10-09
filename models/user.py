"""
User model representing a generic user.
"""

from dataclasses import dataclass


@dataclass
class User:
    """
    Base User class representing a generic user using dataclass.
    """

    id: int
    name: str
    email: str
    password_hash: str
    role: str
