from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    mail: EmailStr

    class Config:
        orm_mode = True


class GetUser(UserBase):
    id: int
    created_time: datetime

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


# AUTH //
class UserLogin(BaseModel):
    mail: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    # class Config:
    #     orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None

    # token_type: str

    class Config:
        orm_mode = True


# short URL Logging //
class ClientOfLinks(BaseModel):
    user_mail: EmailStr
    client_browser: str
    client_os: str
    client_device: str
    client_ip: str
    click_time: datetime

    class Config:
        orm_mode = True
