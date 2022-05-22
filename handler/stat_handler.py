from aiogram import types

from bot_init import *
from time_util.current_time import *


@dp.message_handler(lambda msg: msg.text == "📈 Статистика")
async def stat_handler(message: types.Message):
    userRepo.updateUserTimeOnlineDate(message.from_user.id, current_time())

    await bot.send_message(message.from_user.id, F"📌 Статистика:\n\n"
                                                 F"🔰 Нових користувачів за сьогодні: {userRepo.countAllUserRegToday()}\n"
                                                 F"💬 Сьогодні було в мережі: {userRepo.countAllUserOnlineToday()}\n"
                                                 F"🌐 Всього користувачів за весь час: {userRepo.countAllUser()}\n\n")
