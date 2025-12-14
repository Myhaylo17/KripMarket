import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://root:123%2B456Ab@localhost/kripmarket_db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    future=True
)

Base = declarative_base()

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession, # Використовуємо AsyncSession
    future=True
)

async def get_db() -> AsyncSession:

    async with AsyncSessionLocal() as db:
        try:
            yield db
        except Exception as e:
            logging.error(f"Database session error: {e}")
            await db.rollback()
            raise

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)