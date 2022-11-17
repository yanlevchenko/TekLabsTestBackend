from sqlalchemy.orm import Session
from database.models import Meeting
from schemas.models import DeleteMeetingResponse, DeleteMeetingDto, MeetingDto, CreateMeetingResponse
from .user_crud import user_get_one
from datetime import timedelta
from fastapi import HTTPException, status

def meetings_get_all(db: Session):
    return db.query(Meeting).all()


def meeting_create(db: Session, meeting: MeetingDto):
    try:
        user = user_get_one(db=db, email=meeting.user_email)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )
    for dbmeeting in meetings_get_all(db=db):
        if dbmeeting.start_date <= meeting.date.replace(tzinfo=None) <= dbmeeting.finish_date:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="This time is busy"
            )
    db_meeting = Meeting(user_id=user.id, start_date=meeting.date, finish_date=meeting.date + timedelta(minutes=30))
    db.add(db_meeting)
    db.commit()
    print(f'Meeting ${meeting.date} was created')
    return CreateMeetingResponse(detail='Meeting created.')


def meeting_delete(db: Session, meetingDto: DeleteMeetingDto):
    try:
        user = user_get_one(db=db, email=meetingDto.user_email)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )
    user_meetings = user.meetings
    print(meetingDto.date)
    meeting = None
    for user_meeting in user_meetings:
        if user_meeting.start_date == meetingDto.date.replace(tzinfo=None):
            meeting = user_meeting
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User don't have such meeting"
        )
    db.query(Meeting).filter_by(id=meeting.id).delete()
    db.commit()
    print(f'Meeting ${meetingDto.date} was deleted')
    return DeleteMeetingResponse(detail='User deleted')
