from fastapi import APIRouter
from crud import meetings
from db.db_manager import DBSessionDep
from schemas.meetings import Meeting

router = APIRouter()

@router.post(
    "/create_google_meeting",
    response_model=Meeting
)
async def create_google_meeting(
    user_id: int,
    db_session: DBSessionDep,
):
    res  = await meetings.create_google_meeting(db_session, user_id)
    return res

@router.get(
    "/meetings-list/{user_id}",
    response_model=list[Meeting]
)
async def get_user_meetings(
    user_id: int,
    db_session: DBSessionDep
):

    return await meetings.list_user_meetings(db_session, user_id)
