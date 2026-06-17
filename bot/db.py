import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def get_connection():
    return await asyncpg.connect(os.getenv("DATABASE_URL"))

async def create_habit(user_id: int, name: str):
    conn = await get_connection()
    await conn.execute(
        "INSERT INTO habits (user_id, name) VALUES ($1, $2)",
        user_id, name
    )
    await conn.close()

async def get_habits(user_id: int):
    conn = await get_connection()
    habits = await conn.fetch(
        "SELECT id, name FROM habits WHERE user_id = $1",
        user_id
    )
    await conn.close()
    return habits

async def delete_habit(habit_id: int):
    conn = await get_connection()
    await conn.execute(
        "DELETE FROM habits WHERE id = $1",
        habit_id
    )
    await conn.close()

async def habit_log(user_id: int, habit_id: int):
    conn = await get_connection()
    await conn.execute(
        "INSERT INTO habit_logs (user_id, habit_id) VALUES($1, $2)",
        user_id, habit_id
    )
    await conn.close()

async def is_habit_logged_today(habit_id):
    conn = await get_connection()
    result = await conn.fetchrow(
        "SELECT id FROM habit_logs WHERE habit_id = $1 AND completed_at = CURRENT_DATE",
        habit_id
    )
    await conn.close()
    return result

async def get_stats(user_id, days):
    conn = await get_connection()
    result = await conn.fetch(
        """
        SELECT h.name, COUNT(hl.id) as completed_count
        FROM habits h
        LEFT JOIN habit_logs hl ON h.id = hl.habit_id
            AND hl.completed_at >= CURRENT_DATE - ($2 || ' days')::interval
        WHERE h.user_id = $1
        GROUP BY h.id, h.name
        """,
        user_id, str(days)
    )
    await conn.close()
    return result