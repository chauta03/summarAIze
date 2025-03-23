from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from passlib.context import CryptContext
from db.models import User
from schemas.users import UserResponse
from db.models import User as UserDbCreate

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
    new_user = UserDbCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password
    )
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)  # Refresh to get the new user's ID

    return UserResponse.model_validate(new_user)

async def sign_in(db_session: AsyncSession, email: str, password: str) -> User:
    # Check if the user exists
    result = await db_session.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify the password
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return UserResponse.model_validate(user)