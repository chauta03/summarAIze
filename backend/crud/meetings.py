from db.models import Meeting as MeetingDBModel
from schemas.meetings import Meeting
from fastapi import HTTPException
from services.meetings.google_meet import GoogleMeetServices
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def create_google_meeting(db_session: AsyncSession, user_id: int) -> Meeting:
    # Call the Google Meet service to create a meeting
    google_meet_services = GoogleMeetServices(db_session=db_session, user_id=user_id)
    meeting_info = await google_meet_services.create_google_meet()
    if not meeting_info:
        raise HTTPException(status_code=500, detail="Failed to create Google meeting")
    
    # Extract meeting details
    meeting_id = meeting_info["meeting_id"]
    meeting_url = meeting_info["meeting_url"]
    
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
