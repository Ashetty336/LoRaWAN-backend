# models.py
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserVerify(BaseModel):
    email: EmailStr
    google_id: str

class UserSignUp(BaseModel):
    name:str
    email: EmailStr
    role:str

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    google_id: Optional[str] = None

class UserDetails(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

class UserUpdateDetails(BaseModel):
    id: UUID
    email: str
    name: str
    role: str
    is_active: bool
    created_at: str
    last_login: str