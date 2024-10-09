"""
This module contains Pydantic models for input validation.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, constr


class LoginModel(BaseModel):
    """
    Pydantic model for login input validation.
    """

    email: EmailStr
    password: constr(min_length=8)


class SignupModel(BaseModel):
    """
    Pydantic model for signup input validation.
    """

    name: constr(min_length=2)
    email: EmailStr
    password: constr(min_length=8)


class UpdateStudentModel(BaseModel):
    """
    Pydantic model for updating student profile.
    """

    name: Optional[str] = None
    ssn: Optional[str] = None  # Social Security Number
