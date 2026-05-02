"""API dependencies for dependency injection."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session for API endpoints.
    
    Yields:
        AsyncSession: Database session
    """
    async for session in get_db():
        yield session

# Made with Bob
