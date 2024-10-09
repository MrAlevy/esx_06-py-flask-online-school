"""
This module contains the class model.
"""

from dataclasses import dataclass


@dataclass
class Class:
    """
    Class model representing a class/course in the system.
    """

    id: int
    name: str
    tutor_id: int  # ID of the tutor teaching the class
    student_ids: list = None  # List of student IDs enrolled in the class

    def __post_init__(self):
        if self.student_ids is None:
            self.student_ids = []
