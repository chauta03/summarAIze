from sqlalchemy import (Column, ForeignKey, Integer, String, DateTime)
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
    app_integrations = relationship("AppIntegration", back_populates="user")


class Meeting(Base):
    """Keeps track of meetings"""

    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(100), nullable=False)
    meeting_id = Column(String(150), nullable=True)
    record_url = Column(String(250), nullable=True)
    meeting_url = Column(String(250), nullable=False)
    transcription = Column(String(500), nullable=True)
    summary = Column(String(500), nullable=True)
    duration = Column(Integer, nullable=True)

    user = relationship("User", back_populates="meetings")

class AppIntegration(Base):
    """Keeps track of app integrations for users"""

    __tablename__ = "app_integrations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    app_name = Column(String(150), nullable=False)
    token = Column(String(500), nullable=False)
    refresh_token = Column(String(500), nullable=True)
    expire = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="app_integrations")
