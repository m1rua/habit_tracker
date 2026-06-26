# 🎯 MiruaHabitTracker

Телеграм-бот + Mini App для трекинга привычек. Сделал потому что не захотел платить за премиум в существующих приложениях — написал своё.

[![CI/CD](https://github.com/m1rua/habit_tracker/actions/workflows/deploy.yml/badge.svg)](https://github.com/m1rua/habit_tracker/actions/workflows/deploy.yml)

---

## Что умеет

- Добавить / удалить привычку
- Отметить выполнение (с защитой от двойной отметки за день)
- Статистика выполнения за 30 / 90 / 365 дней с % и цветовой индикацией
- Telegram Mini App с тёмной и светлой темой

## Стек

| Слой | Технологии |
|---|---|
| Бот | Python 3.11, aiogram 2.25, FSM |
| API | FastAPI, uvicorn |
| БД | PostgreSQL 15, asyncpg |
| Инфра | Docker, docker-compose |
| Сервер | Ubuntu 24.04, Nginx, Let's Encrypt |
| CI/CD | GitHub Actions |

## Архитектура

```
Telegram ──► aiogram bot (polling)
               │
Browser ───► Nginx (HTTPS) ──► FastAPI (REST API) ──► PostgreSQL
               │
               └──► Static (Mini App HTML)
```

Три Docker контейнера: `bot`, `api`, `db` — управляются через docker-compose.

## Структура проекта

```
habit_tracker/
├── bot/
│   ├── main.py          # хендлеры бота
│   ├── api.py           # FastAPI endpoints
│   ├── db.py            # функции работы с БД
│   ├── keyboards.py     # клавиатуры
│   ├── static/
│   │   └── index.html   # Telegram Mini App
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── init.sql         # миграции (создание таблиц)
│   └── requirements.txt
└── .github/
    └── workflows/
        └── deploy.yml   # CI/CD pipeline
```

## Локальный запуск

```bash
git clone https://github.com/m1rua/habit_tracker.git
cd habit_tracker/bot
```

Создай `.env` файл:
```
BOT_TOKEN=your_token
DATABASE_URL=postgresql://user:password@db:5432/habits?sslmode=disable
```

Запусти:
```bash
docker compose up --build -d
```

## CI/CD

При каждом `git push` в `main`:

1. **Lint** — flake8 проверяет код
2. **Deploy** — GitHub Actions подключается по SSH и деплоит на сервер

Если линтер упал — деплой не происходит.

## API endpoints

```
GET    /habits              — список привычек
POST   /habits              — создать привычку
DELETE /habits/{id}         — удалить привычку
POST   /habits/{id}/log     — отметить выполнение
GET    /habits/logged-today — отмеченные сегодня
GET    /stats/{days}        — статистика за период
```

## Mini App

Доступна по адресу [miruahabittracker.mooo.com](https://miruahabittracker.mooo.com) и через кнопку в боте [@MiruaHabitTrackerBot](https://t.me/MiruaHabitTrackerBot).
