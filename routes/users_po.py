# Python
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
from models.user import users
# Schemas
from schemas.user_model import UserBase, PasswordMixin, UserLogin, User, UserRegister
# Cryptografy
from cryptography.fernet import Fernet

# Generate key for cryptography
key = Fernet.generate_key()
# Generate fuction fir crypto
crypto_fuction = Fernet(key)

# APIRouter Ini
user = APIRouter()

# Path Operations

## Users

### Register a user
@user.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(
    user: UserRegister = Body(...)
):
    """
    ## Signup a User

    This path operation register a user in the app

    **Parameters**

    - Request body parameter
        - user: UserRegister

    Return a json with the basic user information:

    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    
    # transform the request body in dictionary and save in variable dict
    user_dict = user.dict()
    # user_id and birth_date are not string and use cast for transform in dict
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])
    # Encrypting password
    user_dict["password"] = crypto_fuction.encrypt(user.password.encode("utf-8"))

    # Inserting new user in db
    results = conn.execute(users.insert().values(user_dict))

    return user

### Login a user
@user.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login(
    login_email: EmailStr = Form(...),
    login_password: str = Form(...)
):
    """
    ## login a User

    This path operation login a user in the app

    **Parameters**

    - Request Form parameter
        - user mail: EmailStr -> A user mail
        - password: str -> A password for user mail

    Return a json with the basic user information:

    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    # open file user.json in read mode with utf-8 encoding
    results = read_file(model='users')
    # status user
    #  1 - user and password are correct
    #  2 - User exists but password incorrect
    #  3 - user not exits
    user_status = 3
    for user in results:
        if user['email'] == login_email:
            user_status = 2
            if user['password'] == login_password:
                user_status = 1
                user_result = user

    if user_status == 1:
        return  user_result
    elif user_status == 2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡The Password is incorrect!"
        )
    elif user_status == 3:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This user does not exists!"
        )

### Show all users
@user.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    ## Show all users

    This path operation show all users in the app

    **Parameters**

    - 

    Return a json list with all users in the app with following keys:

    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    results = read_file(model='users')
    return results

### Show a user
@user.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
)
def show_a_user(
    user_id: str = Path(
        ...,
        title="User ID",
        min_length=1,
        description="This is a User ID, It's required",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa8"
    )
):
    """
    ## show a user

    This path operation show a user in the app

    **Parameters**

    - Request Path Parameter
        - user_id: UUID -> User ID

    Return a json with the basic user information:

    - user_id: Str
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    #open file user.json in read mode with utf-8 encoding
    results = read_file(model='users')
    # status user
    #  1 - user exists
    #  2 - user not exits
    user_status = 2
    for user in results:
        if user['user_id'] == user_id:
            user_status = 1
            user_result = user

    if user_status == 1:
        return  user_result
    elif user_status == 2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This user does not exists!"
        )

### Delete a user
@user.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
def delete_a_user(
    user_id: str = Path(
        ...,
        title="User ID",
        min_length=1,
        description="This is a User ID, It's required",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa8"
    )
):
    """
    ## Delete a user

    This path operation delete a user in the app

    **Parameters**

    - Request Path Parameter
        - user_id: Str -> User ID

    Return a json with the basic user information deleted:

    - user_id: Str
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    #open file user.json in read/write mode with utf-8 encoding
    with open("users.json", "r+", encoding="utf-8") as f:
        # read file and take the string and transform as json and loda in result
        results = json.loads(f.read())
        # status user
        #  1 - user exists
        #  2 - user not exits
        user_status = 2
        for user in results:
            if user['user_id'] == user_id:
                user_status = 1
                results.remove(user)
        # move the firts line in file
        f.truncate(0)
        f.seek(0)
        # write in the file and transform a list of dict -results- an a json
        f.write(json.dumps(results))

    if user_status == 1:
        return user
    elif user_status == 2:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="¡This user does not exists!"
    )

### Update a user
@user.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
)
def update_a_user(
    user_id: str = Path(
        ...,
        title="User ID",
        min_length=1,
        description="This is a User ID, It's required",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa4"
    ),
    first_name: str = Form(
        ...,
        title="First Name",
        description="The first name of the user",
        example="Carlos"
    ),
    last_name: str = Form(
        ...,
        title="Last Name",
        description="The last name of the user",
        example="Oliveira"
    ),
    email: EmailStr = Form(
        ...,
        title="Email",
        description="The email of the user",
        example="carlos@example.com"
    )
):
    """
    ## Update a user

    This path operation update a user in the app

    **Parameters**

    - Request Path Parameter
        - user_id: Str -> User ID

    Return a json with the basic user information updated:

    - user_id: Str
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    #open file user.json in read/write mode with utf-8 encoding
    with open("users.json", "r+", encoding="utf-8") as f:
        # read file and take the string and transform as json and loda in result
        results = json.loads(f.read())
        # status user
        #  1 - user exists
        #  2 - user not exits
        user_status = 2
        for user in results:
            if user['user_id'] == user_id:
                user_status = 1
                user['first_name'] = first_name
                user['last_name'] = last_name
                user['email'] = email
                user_result = user
        # move the firts line in file
        f.truncate(0)
        f.seek(0)
        # write in the file and transform a list of dict -results- an a json
        f.write(json.dumps(results))

    if user_status == 1:
        return user_result
    elif user_status == 2:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="¡This user does not exists!"
    )


@user.get("/")
def get_users():
    return conn.execute(users.select()).fetchall

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