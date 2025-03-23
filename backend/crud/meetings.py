from db.models import Meeting as MeetingDBModel
from schemas.meetings import Meeting
from fastapi import HTTPException
from services.meetings.google_meet import GoogleMeetServices
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

google_meet_services = GoogleMeetServices()

async def create_google_meeting(db_session: AsyncSession, user_id: int) -> Meeting:
    # Call the Google Meet service to create a meeting
    meeting_info = google_meet_services.create_google_meet()
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
