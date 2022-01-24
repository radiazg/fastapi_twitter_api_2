# Python
from unittest import result
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
import json
# FastAPI
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Form, Path
from fastapi import HTTPException
# Pydantic
from pydantic import EmailStr
# Connection DB
from config.db import conn
# Models DB
from models.tweet import tweets
# Schemas
from schemas.tweet_model import Tweet

# APIRouter Init
tweet = APIRouter()

# Path Operations

## Tweets

### Show all tweets
@tweet.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweet"]
)
def home():
    """
    ## Show all tweets

    This path operation show all tweets in the app

    **Parameters**

    - 

    Return a json list with all tweets in the app with following keys:

    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - user_by: UUID
    """
    results = conn.execute(tweets.select()).fetchall()
    return results

### Post a tweet
@tweet.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweet"]
)
def post(tweet: Tweet = Body(...)):
    
    """
    ## Post a Tweet

    This path operation post a tweet in the app

    **Parameters**

    - Request body parameter
        - tweet: Tweet

    Return a json with the basic tweet information:

    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - user_by: UUID
    """
    # transform the request body in dictionary and save in variable dict
    tweet_dict = tweet.dict()
    # tweet_id, created_at and update_at are not string and use cast for transform in dict
    tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
    tweet_dict["created_at"] = str(tweet_dict["created_at"])
    tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
    # user_id is not string and use cast for transform in dict
    tweet_dict["user_by"] = str(tweet_dict["user_by"])
    
    # insert tweet in tweets table on db
    results = conn.execute(tweets.insert().values(tweet_dict))

    return tweet

### Show a tweet
@tweet.get(
    path="/tweet/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweet"]
)
def show_a_tweet(
    tweet_id: str = Path(
        ...,
        title="Tweet ID",
        min_length=1,
        description="This is a tweet ID, It's required",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    )
):
    """
    ## show a tweet

    This path operation show a tweet in the app

    **Parameters**

    - Request Path Parameter
        - tweet_id: str -> Tweet ID

    Return a json with the basic tweet information:

    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - user_by: UUID
    """
    # Connect to database and get a user data of table users
    results = conn.execute(tweets.select().where(tweets.c.tweet_id == tweet_id)).first()

    if results is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This tweet does not exists!"
        )
    else:
        return results

### Delete a tweet
@tweet.delete(
    path="/tweet/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweet"]
)
def delete_a_tweet(
    tweet_id: str = Path(
        ...,
        title="Tweet ID",
        min_length=1,
        description="This is a tweet ID, It's required",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa9"
    )
):
    """
    ## delete a tweet

    This path operation delete a tweet in the app

    **Parameters**

    - Request Path Parameter
        - tweet_id: str -> Tweet ID

    Return a json with the basic tweet information deleted:

    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - user_by: UUID
    """
    # Connect to database and get a user data of table users
    results = conn.execute(tweets.select().where(tweets.c.tweet_id == tweet_id)).first()

    # Validate if tweet exists
    if results is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This tweet does not exists!"
        )
    else:
        conn.execute(tweets.delete().where(tweets.c.tweet_id == tweet_id))
        return results

### Update a tweet
@tweet.put(
    path="/tweet/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweet"]
)
def update_a_tweet(
    tweet_id: str = Path(
        ...,
        title="Tweet ID",
        min_length=1,
        description="This is a tweet ID, It's required",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa9"
    ),
    content: str = Form(
        ...,
        title="Content tweet",
        description="The content of tweet",
        example="This tweet has been updated"
    )
):
    """
    ## update a tweet

    This path operation update a tweet in the app

    **Parameters**

    - Request Path Parameter
        - tweet_id: str -> Tweet ID
    - Request Form Parameter
        - content: str -> Content of tweet

    Return a json with the basic tweet information updated:

    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - user_by: UUID
    """
    # Connect to database and get a user data of table users
    results = conn.execute(tweets.select().where(tweets.c.tweet_id == tweet_id)).first()

    # validate if tweet exists
    if results is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="¡This tweet does not exists!"
        )
    else:
        conn.execute(tweets.update().values(content = content, updated_at = datetime.now()).where(tweets.c.tweet_id == tweet_id))
        return conn.execute(tweets.select().where(tweets.c.tweet_id == tweet_id)).first()

