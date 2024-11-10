from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Annotated


class UserBase(BaseModel):
    first_name: str = Field(..., example="Robert", title="First Name")
    last_name: str = Field(..., example="Smith", title="Last Name")
    email: EmailStr = Field(..., example="email@example.com", title="Email")
    password: str = Field(..., example="password", title="Password")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(..., example="email@example.com", title="Email")
    password: Optional[str] = Field(..., example="qwerty", title="Password")
