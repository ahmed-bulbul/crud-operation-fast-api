from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.schemas.user_schema import UserCreate
from passlib.hash import bcrypt
from app.core.logger import logger

# Create user
async def create_user(db: AsyncSession, user: UserCreate):
    try:
        hashed_password = bcrypt.hash(user.password)
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        logger.info(f"User created: {db_user.username} (ID: {db_user.id})")
        return db_user
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error creating user {user.username}: {e}", exc_info=True)
        raise

# Get user by username
async def get_user_by_username(db: AsyncSession, username: str):
    try:
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        logger.info(f"Fetched user by username: {username}")
        return user
    except SQLAlchemyError as e:
        logger.error(f"Error fetching user by username {username}: {e}", exc_info=True)
        raise

# Get user by ID
async def get_user_by_id(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        logger.info(f"Fetched user by ID: {user_id}")
        return user
    except SQLAlchemyError as e:
        logger.error(f"Error fetching user by ID {user_id}: {e}", exc_info=True)
        raise

# Get all users
async def get_users(db: AsyncSession):
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        logger.info(f"Fetched all users, count: {len(users)}")
        return users
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all users: {e}", exc_info=True)
        raise

# Update user
async def update_user(db: AsyncSession, user_id: int, new_data: dict):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalars().first()
        if not db_user:
            logger.warning(f"User not found for update: ID {user_id}")
            return None

        for key, value in new_data.items():
            # Hash password if updating
            if key == "password":
                value = bcrypt.hash(value)
                key = "hashed_password"
            setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)
        logger.info(f"User updated: ID {db_user.id}")
        return db_user
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error updating user ID {user_id}: {e}", exc_info=True)
        raise

# Delete user
async def delete_user(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        db_user = result.scalars().first()
        if not db_user:
            logger.warning(f"User not found for deletion: ID {user_id}")
            return None
        await db.delete(db_user)
        await db.commit()
        logger.info(f"User deleted: ID {user_id}")
        return db_user
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error deleting user ID {user_id}: {e}", exc_info=True)
        raise
