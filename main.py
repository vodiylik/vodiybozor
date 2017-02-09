# Asyncio
import asyncio

# UVLoop
import uvloop

# Asyncpg
from asyncpg import create_pool

# Bot
from bot import bot

# Misc
import os

# Use uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy)


async def run_bot():
    await bot.loop()


async def make_pg_pool():
    dsn = os.environ.get('DATABASE_URL')
    return await create_pool(dsn=dsn, max_size=2)


# Postgres connection pool
loop = asyncio.get_event_loop()
pg_pool = loop.run_until_complete(make_pg_pool())
setattr(bot, 'pg_pool', pg_pool)


if __name__ == '__main__':
    loop.run_until_complete(run_bot())
