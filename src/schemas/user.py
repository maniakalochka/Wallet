from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Annotated


class UserBase(BaseModel):
    first_name: str = Field(..., example="Robert", title="First Name")
    last_name: str = Field(..., example="Smith", title="Last Name")
    username: str = Field(..., example="RobertSmith", title="Username")
    email: EmailStr = Field(..., example="email@example.com", title="Email")
    hashed_password: str = Field(..., example="password", title="Password")

    class Config:
        from_attributes = True
        

class UserCreate(UserBase):
    pass


class UserUpdatePassword(BaseModel):
    password: Optional[str] = Field(..., example="qwerty", title="Password")

class UserLogin(BaseModel):
    username: str = Field(..., example="RobertSmith", title="Username")
    password: str = Field(..., example="password", title="Password")


class UserDeactivate(BaseModel):
    username: str = Field(..., example="RobertSmith", title="Username")
    is_active: bool = Field(..., example=False, title="Is Active")


class SuperUserCreate(UserBase):
    is_admin: bool = Field(..., example=True, title="Is Admin")
