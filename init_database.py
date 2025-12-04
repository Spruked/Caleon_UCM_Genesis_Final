#!/usr/bin/env python3
"""
Database initialization script for Caleon UCM
Creates all required tables for the AGI system
"""
import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base
from models.unanswered_query import UnansweredQuery
from models.caleon import ClusterNode, ClusterEdge, Predicate
from models.vault import VaultLog

async def init_database():
    # Create engines for both databases
    caleon_engine = create_async_engine("sqlite+aiosqlite:///./caleon.db", echo=True)
    vault_engine = create_async_engine("sqlite+aiosqlite:///./vault.db", echo=True)

    # Create tables for Caleon database
    async with caleon_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create tables for Vault database
    async with vault_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database tables created successfully!")
    print("📁 caleon.db - Contains cluster, node, edge, and predicate tables")
    print("📁 vault.db - Contains audit logs and unanswered queries")

    # Close engines
    await caleon_engine.dispose()
    await vault_engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_database())