"""
Tutor class definition.
"""

from dataclasses import dataclass
from .user import User


@dataclass
class Tutor(User):
    """
    Tutor class inheriting from User, representing a tutor user.
    """

    teaching_classes: list = None  # List of class IDs the tutor is teaching
    office_hours: str = None  # Optional office hours information

    def __post_init__(self):
        self.role = "tutor"
        if self.teaching_classes is None:
            self.teaching_classes = []
