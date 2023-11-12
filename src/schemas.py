from datetime import date, datetime
from pydantic import BaseModel, Field


# Contacts 
class ContactBase(BaseModel):
    name: str = Field(max_length=25)


class ContactModel(ContactBase):
    surname: str = Field(max_length=25)
    email: str = Field(max_length=30)
    phone: str = Field(max_length=17)
    birthday: date = Field()


class ContactUpdate(ContactModel):
    favourite: bool


class ContactResponse(ContactBase):
    id: int
    surname: str
    email: str
    phone: str
    birthday: date
    favourite: bool

    class Config:
        orm_mode = True


# Users
class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


# Tokens
class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"