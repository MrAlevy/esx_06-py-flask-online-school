"""
Admin class definition.
"""

from dataclasses import dataclass
from .user import User


@dataclass
class Admin(User):
    """
    Admin class inheriting from User, representing an administrator.
    """

    permissions: list = None  # List of permissions for the admin

    def __post_init__(self):
        self.role = "admin"
        if self.permissions is None:
            self.permissions = []
