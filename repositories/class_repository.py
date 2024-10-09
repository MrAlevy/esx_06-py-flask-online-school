"""
This module contains the repository class for class-related data operations.
For the real app, this class would interact with a database.
"""

from .data_store import classes


class ClassRepository:
    """
    Repository class for class-related data operations.
    """

    @staticmethod
    def create_class(class_obj):
        """
        Add a new class to the data
        """
        classes[class_obj.id] = class_obj

    @staticmethod
    def get_class_by_id(class_id):
        """
        Retrieve a class by its ID.
        """
        return classes.get(class_id)

    @staticmethod
    def update_class(class_id, updated_class):
        """
        Update an existing class in the data store.
        """
        if class_id in classes:
            classes[class_id] = updated_class
            return True
        return False

    @staticmethod
    def delete_class(class_id):
        """
        Delete a class from the data store.
        """
        return classes.pop(class_id, None)

    @staticmethod
    def get_all_classes():
        """
        Retrieve all classes from the data store.
        """
        return list(classes.values())
