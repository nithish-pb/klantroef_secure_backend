from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Auth
class SignupIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Media
class MediaCreate(BaseModel):
    title: str
    type: str = Field(pattern="^(video|audio)$")
    file_url: str

class MediaOut(BaseModel):
    id: int
    title: str
    type: str
    file_url: str
    created_at: datetime

    class Config:
        from_attributes = True
