import uuid

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .connection import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True)
    meetings = relationship("Meeting", back_populates="user")
    

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(ForeignKey('users.id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    start_date = Column(DateTime, unique=True)
    finish_date = Column(DateTime)
    user = relationship("User", back_populates="meetings")


Base.metadata.create_all(engine)