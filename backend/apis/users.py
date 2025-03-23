from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserCreate, UserLogin, UserResponse
from crud.users import sign_up, sign_in
from db.db_manager import DBSessionDep

router = APIRouter()

@router.post("/sign_up", response_model=UserResponse)
async def user_sign_up(
    user: UserCreate,  # Extracts user data from the request body
    db_session: DBSessionDep  # Injects the database session
):
    """
    API endpoint for user sign-up.
    """
    return await sign_up(
        db_session=db_session,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password
    )

@router.post("/sign_in", response_model=UserResponse)
async def user_sign_in(
    credentials: UserLogin,  # Extracts email and password from the request body
    db_session: DBSessionDep  # Injects the database session
):
    """
    API endpoint for user sign-in.
    """
    return await sign_in(
        db_session=db_session,
        email=credentials.email,
        password=credentials.password
    )