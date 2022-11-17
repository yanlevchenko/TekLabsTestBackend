from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.models import UserDto, CreateUserResponse
from utils.user_crud import (
    user_create
)

router = APIRouter(tags=["users"])

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
def create_meeting(user: UserDto, db: Session = Depends(get_db)):
    response = user_create(db=db, user=user)

    print(user.email, 'was created')
    return response
