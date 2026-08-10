from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class SongOut(BaseModel):
    id: int
    title: str
    artist: str
    genre: Optional[str] = None
    duration: Optional[int] = None
    audio_url: Optional[str] = None
    class Config:
        from_attributes = True


class SongCreate(BaseModel):
    title: str
    artist: str
    genre: Optional[str] = None
    duration: Optional[int] = None


class PlaylistCreate(BaseModel):
    name: str


class PlaylistOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True