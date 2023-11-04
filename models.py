import os
import asyncio

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


PG_USER = os.getenv("PG_USER", "app")
PG_PASSWORD = os.getenv("PG_PASSWORD", "1234")
PG_DB = os.getenv("PG_DB", "app")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", 5431)

PG_DSN = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Swapipeople(Base):

    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), index=True)
    birth_year = Column(String(50), index=True)
    eye_color = Column(String(50), index=True)
    films = Column(String(200), index=True)
    gender = Column(String(50), index=True)
    hair_color = Column(String(50), index=True)
    height = Column(String(50), index=True)
    homeworld = Column(String(100), index=True)
    mass = Column(String, index=True)
    skin_color = Column(String(50), index=True)
    species = Column(String(200), index=True)
    starships = Column(String(200), index=True)
    vehicles = Column(String(200), index=True)

async def make_table():
    """Функция делает миграцию в БД и создает таблицы."""

    async with engine.begin() as connection:  # Код создает миграции в БД. Такой код нужен для асинхронного прогр-я.
        await connection.run_sync(Base.metadata.create_all)


async def drop_table():
    """Функция делает миграцию в БД и удаляет таблицы."""

    async with engine.begin() as connection:  # Код удаляет миграции в БД. Такой код нужен для асинхронного прогр-я.
        await connection.run_sync(Base.metadata.drop_all)



async def main():
    await get_async_session(True, True)


if __name__ == '__main__':
    asyncio.run(main())