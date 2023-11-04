# C:\Users\glesh\netology\вебразработка\Asyncio\venv\Scripts\python.exe

import asyncio
#import asyncpg
from aiohttp import ClientSession
import datetime
from more_itertools import chunked 
from models import Session, Swapipeople, engine, Base


CHUNK_SIZE = 10

async def chunked_async(async_iter, size):
    buffer = []
    while True:
        try:
            item = await async_iter.__anext__()
        except StopAsyncIteration:
            break
        buffer.append(item)
        if len(buffer) == size:
            yield buffer
            buffer = []


async def get_person(person_id: int, session: ClientSession):
    async with session.get(f'https://swapi.dev/api/people/{person_id}') as response:
        json_data = await response.json()
        json_data['ID'] = person_id
        return json_data


async def get_item(url, d: dict, key1, key2, session):
    async with session.get(url) as response:
        json_data = await response.json()
        name = json_data[key1]
        d[key2] = name


async def get_items(urls: list, d: dict, key1, key2, session):
    l = []
    for url in urls:
        async with session.get(url) as response:
            json_data = await response.json()
            l.append(json_data[key1])
    l = ', '.join(l)
    d[key2] = l


async def gener():
    async with ClientSession() as session:
        for chunk in chunked(range(1, 120), CHUNK_SIZE):
            cor = [get_person(i, session) for i in chunk]
            results = await asyncio.gather(*cor)
            for result in results:
                if 'detail' not in result:
                    result2 = {key: val for key, val in result.items() if
                               key != 'created' and key != 'edited' and key != 'url'}

                    coro1 = get_item(result['homeworld'], result2, 'name', 'homeworld', session)
                    coro2 = get_items(result['films'], result2, 'title', 'films', session)
                    coro3 = get_items(result['species'], result2, 'name', 'species', session)
                    coro4 = get_items(result['starships'], result2, 'name', 'starships', session)
                    coro5 = get_items(result['vehicles'], result2, 'name', 'vehicles', session)
                    res = await asyncio.gather(coro1, coro2, coro3, coro4, coro5)
                    yield result2


async def insert_people(people_chunk):
    async with Session() as session:
        session.add_all([Swapipeople(json=item) for item in people_chunk])
        await session.commit()


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    async for chunk in chunked_async(gener(), CHUNK_SIZE):
        asyncio.create_task(insert_people(chunk))
    tasks = set(asyncio.all_tasks()) - {asyncio.current_task()}
    for task in tasks:
        await task


if __name__ == '__main__':
    start = datetime.now()
    asyncio.run(main())
    print(datetime.now() - start)