# Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
import json
# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr, Field

# Tweet Models

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256,
        example='This tweet is a example for FastAPI'
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    user_by: UUID = Field(...)