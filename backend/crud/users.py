from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, Response
from passlib.context import CryptContext
from db.models import User
from schemas.users import UserResponse, UserUpdate

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def sign_up(db_session: AsyncSession, first_name: str, last_name: str, email: str, password: str) -> User:
    # Check if the user already exists
    result = await db_session.execute(select(User).where(User.email == email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    # Hash the password
    hashed_password = pwd_context.hash(password)

    # Create a new user
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password
    )
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)  # Refresh to get the new user's ID

    return UserResponse.model_validate(new_user)

async def sign_in(db_session: AsyncSession, email: str, password: str, response: Response) -> UserResponse:
    # Check if the user exists
    result = await db_session.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify the password
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Save user information in a session (e.g., using cookies)
    response.set_cookie(key="user_id", value=user.id, httponly=True)

    return UserResponse.model_validate(user)

async def logout(response: Response):

    # Delete the user_id cookie to log the user out
    response.delete_cookie(key="user_id")
    return {"message": "User logged out successfully"}

async def update_user(db_session: AsyncSession, user_id: int, update_data: UserUpdate) -> UserResponse:
    # Fetch the user from the database
    result = await db_session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's fields using the UserUpdate model
    update_dict = update_data.model_dump(exclude_unset=True)  # Only update fields that are provided
    for key, value in update_dict.items():
        if hasattr(user, key) and key != "password":  # Exclude password updates here
            setattr(user, key, value)

    # If password is being updated, hash it
    if "password" in update_dict:
        user.password = pwd_context.hash(update_dict["password"])

    # Commit the changes
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Return the updated user details
    return UserResponse.model_validate(user)
