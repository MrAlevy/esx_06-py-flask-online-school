"""
This module contains the repository class for user-related data operations.
For the real app, this class would interact with a database.
"""

from .data_store import users


class UserRepository:
    """
    Repository class for user-related data operations.
    """

    users = {}  # In-memory store for users

    @staticmethod
    def add_user(user):
        """
        Add a new user to the data store.
        """
        users[user.id] = user

    @staticmethod
    def get_user_by_email(email):
        """
        Retrieve a user by their email address.
        """
        return next((u for u in users.values() if u.email == email), None)

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieve a user by their ID.
        """
        return users.get(user_id)
