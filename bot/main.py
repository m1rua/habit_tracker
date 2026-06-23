import logging
from db import create_habit, get_habits, delete_habit, habit_log, is_habit_logged_today, get_stats
from keyboards import main_menu, habits_delete_keyboard, habits_log_keyboard, stats_keyboard
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
import os

logging.basicConfig(level=logging.INFO)

load_dotenv()
print("TOKEN: ", os.getenv("BOT_TOKEN"))
bot = Bot(token=os.getenv("BOT_TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)
print("Bot started")

class HabitForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_delete = State()

#команды
@dp.message_handler(commands=["start"])
async def cmd_start(message:Message):
    await message.answer("привет, я твой трекер привычек🎯", reply_markup=main_menu)



@dp.message_handler(commands=["add"])
async def cmd_add(message: Message):
    try:
        name = message.text.split(maxsplit=1)[1]
        await create_habit(message.from_user.id, name)
        await message.answer(f"Привычка '{name}' добавлена")
    except Exception as e:
        print("ОШИБКА:", e)
        await message.answer(f"Ошибка: {e}")


@dp.message_handler(commands=["list"])
async def cmd_list(message:Message):
    habits = await get_habits(message.from_user.id)
    if not habits:
        await message.answer("у тебя нет привычек")
        return
    text = ""
    for habit in habits:
        text += f"{habit['id']}. {habit['name']}\n"
    await message.answer(text)



@dp.message_handler(commands=["delete"])
async def cmd_delete(message:Message):
    habit_id = int(message.text.split(maxsplit = 1)[1])
    await delete_habit(habit_id)
    await message.answer ("привычка удалена")



#кнопки
@dp.message_handler(Text(equals = "📋 Мои привычки"))
async def btn_list(message: Message):
    habits = await get_habits(message.from_user.id)
    if not habits:
        await message.answer("у тебя нет привычек")
        return
    text = ""
    for habit in habits:
        text += f"{habit['id']}. {habit['name']}\n"
    await message.answer(text)



@dp.message_handler(Text(equals = "➕ Добавить привычку"))
async def btn_add (message:Message):
    await HabitForm.waiting_for_name.set()
    await message.answer("Напиши название привычки:")

@dp.message_handler(state=HabitForm.waiting_for_name)
async def habit_name_entered(message:Message, state: FSMContext):
    name = message.text
    await create_habit(message.from_user.id, name)
    await state.finish()
    await message.answer(f"Привычка '{name}' добавлена 🎯")


@dp.message_handler(Text(equals = "🗑 Удалить привычку"))
async def btn_delete(message:Message):
    habits = await get_habits(message.from_user.id)
    print("привычки:", habits)
    if not habits:
        await message.answer("у тебя нет привычек")
        return
    await message.answer("какую привычку удалить?", reply_markup=habits_delete_keyboard(habits))


@dp.callback_query_handler(lambda c: c.data.startswith("delete_"))
async def process_delete(callback: CallbackQuery):
    habit_id = int(callback.data.split("_")[1])
    await delete_habit(habit_id)
    await callback.message.answer("привычка удалена 🗑")
    await callback.answer()


@dp.message_handler(Text(equals = "✅ Отметить привычку"))
async def btn_log(message:Message):
    habits = await get_habits(message.from_user.id)
    print("привычки:", habits)
    if not habits:
        await message.answer ("у тебя нет привычек")
        return
    await message.answer("выполнение привычки", reply_markup = habits_log_keyboard (habits))


@dp.callback_query_handler(lambda c: c.data.startswith("log_"))
async def process_log(callback: CallbackQuery):
    habit_id = int(callback.data.split("_")[1])
    already_logged = await is_habit_logged_today(habit_id)
    if already_logged:
        await callback.message.answer("уже отмечено")
        await callback.answer()
        return
    else:
        await habit_log(callback.from_user.id, habit_id)
        await callback.message.answer("привычка выполнена!")
        await callback.answer()


@dp.message_handler(Text(equals="📊 Статистика"))
async def btn_stats(message: Message):
    await message.answer("за какой период?", reply_markup=stats_keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("stats_"))
async def process_stats(callback: CallbackQuery):
    days = int(callback.data.split("_")[1])
    stat = await get_stats(callback.from_user.id, days)
    text = f"📊 Статистика за {days} дней:\n\n"
    for row in stat:
        percent = round(row['completed_count'] / days * 100)
        if percent >= 80:
            emoji = "🟢"
        elif percent >=50:
            emoji = "🟡"
        else:
            emoji = "🔴"
        text += f"{emoji} {row['name']} — {percent}% выполнения\n"
    await callback.message.answer(text)
    await callback.answer()




    
@dp.message_handler()
async def any_message(message: Message):
    print("получил сообщение", message.text)

if __name__ == "__main__":
    print("polling..")
    executor.start_polling(dp)