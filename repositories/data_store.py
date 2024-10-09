# pylint: skip-file # Skip because this is a simulation for data store and lacks real implementation details

"""
This module contains the in-memory data stores for the application.
For the real app, these would be replaced with a database.
"""

from models.student import Student
from models.tutor import Tutor
from models.admin import Admin
from models.class_model import Class
from services.authentication import hash_password

# In-memory data stores simulating a database
users = {}
students = {}
tutors = {}
admins = {}
classes = {}


def initialize_data():
    """
    Function to initialize the data store with sample data.
    """
    password_hash = hash_password("Password123")

    # Create a sample student
    student = Student("1", "John Doe", "student@example.com", password_hash)
    students[student.id] = student
    users[student.id] = student

    # Create a sample tutor
    tutor = Tutor("2", "Jane Smith", "tutor@example.com", password_hash)
    tutors[tutor.id] = tutor
    users[tutor.id] = tutor

    # Create a sample admin
    admin = Admin("3", "Admin User", "admin@example.com", password_hash)
    admins[admin.id] = admin
    users[admin.id] = admin

    # Create a sample class
    class_id = "101"
    sample_class = Class(class_id, "Introduction to Python", tutor.id)
    classes[class_id] = sample_class
    tutor.teaching_classes.append(class_id)
