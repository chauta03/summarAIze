from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.orm import relationship

from db.db_manager import Base

class User(Base):
    """Keeps track of users"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)

    meetings = relationship("Meeting", back_populates="user")


class Meeting(Base):
    """Keeps track of meetings"""

    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(100), nullable=False)
    meeting_id = Column(String(150), nullable=False)
    meeting_url = Column(String(250), nullable=False)

    user = relationship("User", back_populates="meetings")
