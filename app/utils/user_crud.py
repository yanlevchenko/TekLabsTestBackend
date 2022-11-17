from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from database.models import User
from schemas.models import UserDto, CreateUserResponse


def user_create(db: Session, user: UserDto):
    db_user = User(email=user.email)
    try:
        db.add(db_user)
        db.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Such user already exists"
        )
    db.refresh(db_user)
    return CreateUserResponse(detail="User created")

def user_get_one(db: Session, email: str):
    return db.query(User).filter_by(email=email).one()

def users_get_all(db: Session):
    return db.query(User).all()

