from datetime import date
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    email: str
    phone: str
    birthday: date


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date

    class Config:
        orm_mode = True