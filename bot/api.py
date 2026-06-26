from fastapi import FastAPI
from db import get_habits, create_habit, delete_habit, habit_log, get_stats

app = FastAPI()

@app.get("/habits")
async def api_get_habits(user_id: int):
    habits = await get_habits(user_id)
    return habits

@app.post("/habits")
async def api_create_habit(user_id: int, name: str):
    habits = await create_habit(user_id, name)
    return habits

@app.delete("/habits/{habit_id}")
async def api_delete_habit(habit_id: int):
    result = await delete_habit(habit_id)
    return result

@app.post("/habits/{habit_id}/log")
async def api_habit_log(user_id: int, habit_id: int):
    result = await habit_log(user_id, habit_id)
    return result

@app.get("/stats/{days}")
async def api_get_stats(user_id: int, days:int):
    result = await get_stats(user_id, days)
    return result

@app.get("/habits/logged-today")
async def api_logged_today(user_id: int):
    from db import get_logged_today
    result = await get_logged_today(user_id)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port=8000)