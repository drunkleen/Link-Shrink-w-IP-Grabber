from pydantic import BaseModel
from datetime import datetime
from app.schemas import userschema


class URLBase(BaseModel):
    title: str
    url: str


class GetURL(URLBase):
    id: int
    created_time: datetime
    owner_id: int
    owner: userschema.UserBase

    class Config:
        orm_mode = True


class URLOut(GetURL):
    shorten_url: str

    class Config:
        orm_mode = True


class URLCreate(URLBase):
    pass

    class Config:
        orm_mode = True


class URLLogOUT(BaseModel):
    client_ip: str
    client_browser: str
    client_os: str
    client_device: str
    click_time: datetime

    class Config:
        orm_mode = True
