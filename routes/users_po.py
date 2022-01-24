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

# Generate key for encrypting
key = Fernet.generate_key()

# Generate fuction for encrypting and decrypting
crypto_fuction = Fernet(key)

# APIRouter Init
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
    #user_dict["password"] = crypto_fuction.encrypt(user.password.encode("utf-8"))

    # Inserting new user into users table in db
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
    # select the user data from users tables where loging_mail equal a email
    results = conn.execute(users.select().where(users.c.email == login_email)).first()

    # status user
    #  1 - user and password are correct
    #  2 - User exists but password incorrect
    #  3 - user not exits    
    user_status = 2

    if results is None:
        user_status = 3
    else:
        # validate the password input with password decrypting user on database
        if results["password"] == login_password:
            user_status = 1
            user_result = results

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
    # Connect to database and  get all data of table with fetchall property
    results = conn.execute(users.select()).fetchall()
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

    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    # Connect to database and get a user data of table users
    results = conn.execute(users.select().where(users.c.user_id == user_id)).first()
    
    # status user
    #  1 - user exists
    #  2 - user not exits
    user_status = 1

    if results is None:
        user_status = 2
    
    if user_status == 1:
        return  results
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

    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    # status user
    #  1 - user exists
    #  2 - user not exits
    user_status = 1
    # Connect to database and get a user data of table users
    user_to_delete = conn.execute(users.select().where(users.c.user_id == user_id)).first()

    # Validate if user exist
    if user_to_delete is None:
        user_status = 2

    # Validate the return
    if user_status == 1:
        # delete the user into database and return the user deleted
        conn.execute(users.delete().where(users.c.user_id == user_id))
        return user_to_delete
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

    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    # status user
    #  1 - user exists
    #  2 - user not exits
    user_status = 1
    user_to_update = conn.execute(users.select().where(users.c.user_id == user_id)).first()

    # Validate if user exist
    if user_to_update is None:
        user_status = 2

    if user_status == 1:
        conn.execute(users.update().values(first_name = first_name, last_name = last_name, email = email).where(users.c.user_id == user_id))
        return conn.execute(users.select().where(users.c.user_id == user_id)).first()
    elif user_status == 2:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="¡This user does not exists!"
    )
