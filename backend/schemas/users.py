from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    """
    Schema for user sign-up.
    """
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Schema for user sign-in.
    """
    email: EmailStr
    password: str
    
class UserUpdate(BaseModel):
    """
    Schema for user update.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    password: str
    
class UserResponse(BaseModel):
    """
    Schema for user response (excluding sensitive fields like password).
    """
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: str
    email: EmailStr