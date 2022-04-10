from aiogram import types, Dispatcher
from __main__ import bot


async def startTest_handler(message: types.Message):
    bot.send_message(message.from_user.id, 'Presed 1')


def register_handlers_main_menu(dp: Dispatcher):
    dp.register_message_handler(startTest_handler, lambda msg: msg.text == "📝 Почати тест")
