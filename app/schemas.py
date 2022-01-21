import typing
from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    email: str

class UserAuthenticate(UserBase):
    public_id: typing.Optional[str]
    password: str

class UserInfoBase(UserBase):    
    name: str
    organization: str
    created_on : typing.Optional[date]
    is_active : typing.Optional[int]

class UserCreate(UserInfoBase):   
    email_varification_code : typing.Optional[str]
    password: str

class UserInfo(UserInfoBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    public_id: str = None