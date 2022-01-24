# Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
import json
# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr, Field

# Users Models

class PasswordMixin(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        max_length=15,
        example='password'
    )

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(
        ..., 
        example='ricardo@example.com'
    )

class UserLogin(UserBase, PasswordMixin):
    pass

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Ricardo'
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Diaz'
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User, PasswordMixin):
    pass