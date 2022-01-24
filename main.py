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
from routes.users_po import user


app = FastAPI(
    title="Twitter API Model on FastAPI",
    description="This is second version of Twitter API, a platzi work",
    version="0.2.0",
    openapi_tags=[{
        "name": "Users",
        "description": "User Path Operations"
    }
    ]
)

app.include_router(user)

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
    by: UUID = Field(...)

## Tweets

### Show all tweets
@app.get(
    path="/tweet",
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
    - by: User
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    results = read_file(model='tweets')
    return results

### Post a tweet
@app.post(
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
    - by: User
    """
    #open file tweets.json in read/write mode with utf-8 encoding
    with open("tweets.json", "r+", encoding="utf-8") as f:
        # read file and take the string and transform as json and loda in result
        results = json.loads(f.read())
        # transform the request body in dictionary and save in variable dict
        tweet_dict = tweet.dict()
        # tweet_id, created_at and update_at are not string and use cast for transform in dict
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        # user_id and birth_date are not string and use cast for transform in dict
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

        # add user dictionary to results variable
        results.append(tweet_dict)

        # move the firts line in file
        f.truncate(0)
        f.seek(0)
        # write in the file and transform a list of dict -results- an a json
        f.write(json.dumps(results))
        return tweet

### Show a tweet
@app.get(
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

    - tweet_id: str
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - by: User
    """
    #open file tweets.json in read mode with utf-8 encoding
    results = read_file(model='tweets')
    # tweet status
    #  1 - tweet exists
    #  2 - tweet not exits
    tweet_status = 2
    for tweet in results:
        if tweet['tweet_id'] == tweet_id:
            tweet_status = 1
            tweet_result = tweet

    if tweet_status == 1:
        return  tweet_result
    elif tweet_status == 2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This tweet does not exists!"
        )

### Delete a tweet
@app.delete(
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

    - tweet_id: str
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - by: User
    """
    #open file tweets.json in read/write mode with utf-8 encoding
    with open("tweets.json", "r+", encoding="utf-8") as f:
        # read file and take the string and transform as json and loda in result
        results = json.loads(f.read())
        # tweet status
        #  1 - tweet exists
        #  2 - tweet not exits
        tweet_status = 2
        for tweet in results:
            if tweet['tweet_id'] == tweet_id:
                tweet_status = 1
                tweet_result = tweet
                results.remove(tweet)
        # move the firts line in file
        f.truncate(0)
        f.seek(0)
        # write in the file and transform a list of dict -results- an a json
        f.write(json.dumps(results))

    if tweet_status == 1:
        return tweet_result
    elif tweet_status == 2:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="¡This tweet does not exists!"
    )

### Update a tweet
@app.put(
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

    - tweet_id: str
    - content: str
    - created_at: datetime
    - updated_at: datetime
    - by: User
    """
    #open file tweets.json in read/write mode with utf-8 encoding
    with open("tweets.json", "r+", encoding="utf-8") as f:
        # read file and take the string and transform as json and loda in result
        results = json.loads(f.read())
        # tweet status
        #  1 - tweet exists
        #  2 - tweet not exits
        tweet_status = 2
        for tweet in results:
            if tweet['tweet_id'] == tweet_id:
                tweet_status = 1
                tweet['content'] = content
                tweet['updated_at'] = str(datetime.now())
                tweet_result = tweet
        # move the firts line in file
        f.truncate(0)
        f.seek(0)
        # write in the file and transform a list of dict -results- an a json
        f.write(json.dumps(results))

    if tweet_status == 1:
        return tweet_result
    elif tweet_status == 2:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="¡This tweet does not exists!"
    )

## Aditional functions

### read a files
def read_file(model: str):
    """
    ## Read File JSON

    This fuction read a file .json

    **Parameters**

    - Name model : str

    Return a json
    """
    #open file .json in read mode with utf-8 encoding
    f = open(model + '.json', 'r', encoding='utf-8')
    
    # read file and take the string and transform as json and load in result
    results = json.loads(f.read())
    f.close()
    return results