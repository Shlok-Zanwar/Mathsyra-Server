from pydantic import BaseModel
from typing import  Optional, List


class BaseModelPlus (BaseModel):
    class Config:
        orm_mode = True


class UserSignUp (BaseModel):
    name: str
    email: str
    password: str
    username: str


class UserLogIn(BaseModel):
    username: str
    password: str


class VerifyUser(BaseModel):
    id: int
    otp: int


class SaveProfile(BaseModel):
    name: str
    email: str
    password: str
    username: str
    phone_no: Optional[int] = None
    school: Optional[str] = None


class ShowUser(BaseModelPlus):
    name: str
    username: str
    email: str
    verification: dict
