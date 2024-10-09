"""
Student class definition.
"""

from dataclasses import dataclass
from .user import User


@dataclass
class Student(User):
    """
    Student class inheriting from User, representing a student user.
    """

    enrolled_classes: list = None  # List of class IDs the student is enrolled in
    grades: dict = None  # Dictionary mapping class IDs to grades
    ssn_encrypted: str = None  # Encrypted SSN field

    def __post_init__(self):
        self.role = "student"
        if self.enrolled_classes is None:
            self.enrolled_classes = []
        if self.grades is None:
            self.grades = {}
