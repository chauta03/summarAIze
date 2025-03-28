from fastapi import APIRouter, Response, Depends, HTTPException
from schemas.users import UserCreate, UserLogin, UserResponse, UserUpdate
from crud.users import sign_up, sign_in, logout, update_user
from db.db_manager import DBSessionDep
from apis.sessions import get_current_user
from db.models import User
from schemas.users import UserResponse

router = APIRouter()

@router.post("/sign_up", response_model=UserResponse)
async def user_sign_up(
    user: UserCreate,
    db_session: DBSessionDep
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
    credentials: UserLogin,
    db_session: DBSessionDep,
    response: Response
):
    """
    API endpoint for user sign-in.
    """
    return await sign_in(
        db_session=db_session,
        email=credentials.email,
        password=credentials.password,
        response=response
    )
    
@router.post("/logout")
async def user_log_out(response: Response):
    return await logout(response)

@router.get("/user_info")
async def get_user_info(
    current_user: User = Depends(get_current_user),
):
    if current_user:
        return UserResponse.model_validate(current_user)
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/update_user", response_model=UserResponse)
async def user_update(
    update_data: UserUpdate,
    db_session: DBSessionDep,
    current_user: User = Depends(get_current_user),
):
    """
    API endpoint for updating user details.
    """
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Call the update_user function
    updated_user = await update_user(
        db_session=db_session,
        user_id=current_user.id,
        update_data=update_data
    )

    return updated_user
