from fastapi import APIRouter, Depends
from crud import meetings
from db.db_manager import DBSessionDep
from schemas.meetings import Meeting
from apis.sessions import get_current_user
from db.models import User

router = APIRouter()

@router.post(
    "/create_google_meeting",
    response_model=Meeting
)
async def create_google_meeting(
    db_session: DBSessionDep,
    current_user: User = Depends(get_current_user),
):
    res  = await meetings.create_google_meeting(db_session, current_user.id)
    return res

@router.get(
    "/meetings-list",
    response_model=list[Meeting]
)
async def get_user_meetings(
    db_session: DBSessionDep,
    current_user: User = Depends(get_current_user),
):

    return await meetings.list_user_meetings(db_session, current_user.id)
