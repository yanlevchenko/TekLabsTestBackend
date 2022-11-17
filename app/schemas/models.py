from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class MeetingDto(BaseModel):
    date: datetime
    user_email: str

    class Config:
        orm_mode = True

class CreateMeetingResponse(BaseModel):
    detail: str

    class Config:
        orm_mode = True

class UserDto(BaseModel):
    email: str

    class Config:
        orm_mode = True

class DeleteMeetingDto(BaseModel):
    date: datetime
    user_email: str

    class Config:
        orm_mode = True

class DeleteMeetingResponse(BaseModel):
    detail: str

class CreateUserResponse(BaseModel):
    detail: str

    class Config:
        orm_mode = True