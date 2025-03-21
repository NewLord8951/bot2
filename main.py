import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привеееет!')
    logger.info(f'Пользователь {(
        message.from_user.full_name, message.from_user.id)}, запустил бота')


@dp.message()
async def echo(message: types.Message):
    text = message.text

    if text in ['Привет', 'привет', 'hi', 'hello']:
        await message.answer('И тебе привеееееееет!')
    elif text in ['Пока', 'пока', 'До свидания']:
        await message.answer('И тебе пока!, (печально что ты уходишь...)')
    else:
        await message.answer(message.text)


async def main():
    logger.add('file.log',
               format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               rotation='3 days',
               backtrace=True,
               diagnose=True)
    await dp.start_polling(bot)

asyncio.run(main())
