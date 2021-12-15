from aiogram import  executor
from dispatcher import dp
from db import BotDB
import handlers

BotDB = BotDB('telbot_users_follow.db')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)