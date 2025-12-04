from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Database URLs
CALI_X_ONE_DB_URL = os.getenv("CALI_X_ONE_DB_URL", "sqlite+aiosqlite:///./caleon.db")
VAULT_DB_URL = os.getenv("VAULT_DB_URL", "sqlite+aiosqlite:///./vault.db")

# Create engines
caleon_engine = create_async_engine(CALI_X_ONE_DB_URL, echo=False)
vault_engine = create_async_engine(VAULT_DB_URL, echo=False)

# Create session factories
CaleonSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=caleon_engine, class_=AsyncSession)
VaultSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=vault_engine, class_=AsyncSession)

async def get_caleon_db() -> AsyncSession:
    async with CaleonSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_vault_db() -> AsyncSession:
    async with VaultSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()