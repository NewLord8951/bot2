import asyncio
import os
import sqlite3
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

dp = Dispatcher()


def add_user(user_id, username):
    conn = sqlite3.connect('hacker.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (\
        user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()
        print(f'Пользователь {username} ({user_id}) добавлен в базу данных.')
    except sqlite3.IntegrityError as e:
        print(e)
    finally:
        conn.close()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Здорово корова!')
    logger.info(f'Пользователь {(
        message.from_user.full_name, message.from_user.id)}, запустил бота')
    username = message.from_user.username
    user_id = message.from_user.id

    add_user(user_id, username)


@dp.message(Command("show"))
async def show_info(message: types.Message):
    conn = sqlite3.connect('hacker.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hacker")
    rows = cursor.fetchall()
    for row in rows:
        logger.info(row)
        await message.answer(f"{row}")


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    logger.add('file.log',
               format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               rotation='3 days',
               backtrace=True,
               diagnose=True)
    conn = sqlite3.connect('hacker.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hacker (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id INTEGER NOT NULL
    )
    ''')
    bot = Bot(token=os.getenv('TOKEN'))
    await dp.start_polling(bot)

asyncio.run(main())
