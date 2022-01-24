# Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
import json

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr, Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Form, Path
from fastapi import HTTPException

# Import Path Operations
from routes.users_po import user
from routes.tweets_po import tweet


app = FastAPI(
    title="Twitter API Model on FastAPI",
    description="This is second version of Twitter API, a platzi work",
    version="0.2.0",
    openapi_tags=[{
        "name": "Users",
        "description": "User Path Operations"
    },
    {
        "name": "Tweet",
        "description": "Tweets Path Operations"
    }
    ]
)

app.include_router(user)
app.include_router(tweet)