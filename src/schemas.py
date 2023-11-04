from datetime import datetime
from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    name: str = Field(max_length=25)


class ContactModel(ContactBase):
    surname: str = Field(max_length=25)
    email: str = Field(max_length=30)
    phone: str = Field(max_length=17)
    birthday: datetime = Field()


class ContactUpdate(ContactModel):
    favourite: bool


class ContactResponse(ContactBase):
    id: int
    surname: str
    email: str
    phone: str
    birthday: datetime
    favourite: bool

    class Config:
        orm_mode = True