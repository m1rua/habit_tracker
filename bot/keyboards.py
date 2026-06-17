from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("📋 Мои привычки"))
main_menu.add(KeyboardButton("➕ Добавить привычку"))
main_menu.add(KeyboardButton("🗑 Удалить привычку"))
main_menu.add(KeyboardButton ("✅ Отметить привычку"))
main_menu.add(KeyboardButton ("📊 Статистика"))

stats_keyboard = InlineKeyboardMarkup()
stats_keyboard.add(
    InlineKeyboardButton("30 дней", callback_data="stats_30"),
    InlineKeyboardButton("90 дней", callback_data="stats_90"),
    InlineKeyboardButton("365 дней", callback_data="stats_365")
)


def habits_delete_keyboard(habits):
    keyboard = InlineKeyboardMarkup()
    for habit in habits:
        keyboard.add(InlineKeyboardButton(text=habit['name'], callback_data=f"delete_{habit['id']}"))
    return keyboard


def habits_log_keyboard(habits):
    keyboard = InlineKeyboardMarkup()
    for habit in habits:
        keyboard.add(InlineKeyboardButton(
            text=habit['name'],
            callback_data=f"log_{habit['id']}"
        ))
    return keyboard

