from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.models import DeleteMeetingResponse, DeleteMeetingDto, MeetingDto, CreateMeetingResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from decouple import config
from utils.meeting_crud import (
    meeting_create,
    meeting_delete,
    meetings_get_all
)
import pytz
from typing import List


router = APIRouter(tags=["meetings"])

conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_USERNAME"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Yan Levchenko",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=CreateMeetingResponse)
def create_meeting(background_tasks: BackgroundTasks, meeting: MeetingDto, db: Session = Depends(get_db)):
    result = meeting_create(db=db, meeting=meeting)

    message = MessageSchema(
    subject="Meeting booking",
    #add John email to recipients list
    recipients=[EmailStr(meeting.user_email)],
    body="Meeting booking was successfully made.",
    subtype=MessageType.plain)

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message)

    return result


@router.delete(
    "/delete", status_code=status.HTTP_200_OK, response_model=DeleteMeetingResponse
)
def delete_meeting(meeting: DeleteMeetingDto, db: Session = Depends(get_db)):
    print(meeting.date)
    result = meeting_delete(db=db, meetingDto=meeting)
    return result

@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[MeetingDto])
def get_all_posts(db: Session = Depends(get_db)):
    result = list(map(lambda meeting: MeetingDto(date=meeting.start_date, user_email=meeting.user.email), meetings_get_all(db=db)))
    print('get all meetings', result)
    return result
