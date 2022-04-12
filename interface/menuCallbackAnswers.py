from aiogram import types, Dispatcher


async def startTest_handler(message: types.Message):
    from __main__ import bot
    await bot.answer_callback_query()
    await bot.send_message(message.from_user.id, 'Pressed 1')


def register_handlers_main_menu(dp: Dispatcher):
    dp.register_message_handler(startTest_handler, lambda msg: msg.text == "📝 Почати тест")
