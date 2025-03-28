from db.models import Meeting as MeetingDBModel
from schemas.meetings import Meeting
from fastapi import HTTPException
from services.meetings.google_meet import GoogleMeetServices
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from services.ai import transcriptionAgent
from services.ai import geminiAgent
import os

async def create_google_meeting(db_session: AsyncSession, user_id: int) -> Meeting:
    # Call the Google Meet service to create a meeting
    google_meet_services = GoogleMeetServices(db_session=db_session, user_id=user_id)
    meeting_info = await google_meet_services.create_google_meet()
    if not meeting_info:
        raise HTTPException(status_code=500, detail="Failed to create Google meeting")
    
    # Extract meeting details
    meeting_id = meeting_info["meeting_id"]
    meeting_url = meeting_info["meeting_uri"]
    
    # Create a new Meeting database object
    meeting = MeetingDBModel(user_id=user_id, type="google", meeting_id=meeting_id, meeting_url=meeting_url)
    db_session.add(meeting)
    await db_session.commit()
    await db_session.refresh(meeting)  # Refresh the instance to get the updated data from the database
    
    # Convert the SQLAlchemy object to a Pydantic model and return it
    return Meeting.model_validate(meeting)

async def list_user_meetings(db_session: AsyncSession, user_id: int) -> list[Meeting]:
    # Query the database for meetings belonging to the user
    result = await db_session.execute(select(MeetingDBModel).where(MeetingDBModel.user_id == user_id))
    meetings = result.scalars().all()

    # Convert the SQLAlchemy objects to Pydantic models
    return [Meeting.model_validate(meeting) for meeting in meetings]

async def get_meeting_summary(meeting_id: str, db_session: AsyncSession, user_id: int):
    google_meet_services = GoogleMeetServices(db_session=db_session, user_id=user_id)
    return await google_meet_services.summarize_meeting(meeting_id=meeting_id)


async def save_meeting_recording(
    db_session: AsyncSession,
    user_id: int,
    type: str,
    meeting_url: str,
    meeting_id: str | None,
    transcription: str,
    summary: str,
    duration: str,
    created_at: str
) -> Meeting:
    try:
        # Create a new Meeting database object
        meeting = MeetingDBModel(
            user_id=user_id,
            type=type,
            meeting_id=meeting_id,
            meeting_url=meeting_url,
            transcription=transcription,
            summary=summary,
            duration=duration,
            created_at=created_at
        )
        
        # Add the meeting to the session and commit to the database
        db_session.add(meeting)
        await db_session.commit()
        await db_session.refresh(meeting)  # Refresh the instance to get the updated data from the database
        
        # Convert the SQLAlchemy object to a Pydantic model and return it
        return Meeting.model_validate(meeting)  # Assuming model_validate is defined in Pydantic model Meeting

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving meeting recording: {str(e)}")