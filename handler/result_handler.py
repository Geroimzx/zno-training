from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_init import *
from state.FSMResult import *
from keyboard.inline_keyboard import *

from datetime import datetime
import pytz


@dp.message_handler(lambda msg: msg.text == "🗂 Мої результати", state="*")
async def result_handler(message: types.Message):
    await FSMResult.chooseResult.set()
    await bot.send_message(message.from_user.id, "📑 Список результатів:", reply_markup=init_user_test_button_list(message.from_user.id))


@dp.callback_query_handler(lambda msg: True, state=FSMResult.chooseResult)
async def result_view_handler(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = event
        data['user_test_id'] = event.data.split('_')[1]
    await FSMResult.next()
    async with state.proxy() as data:
        user_test = testRepo.findUserTestWithTestNameByUserTestId(str(data['user_test_id']))
        start_time = user_test[3]
        finish_time = user_test[4]
        print(user_test)
        user_data_parsed_list = F"\n📝 Назва тесту:\n{str(user_test[8])}" \
                                F"\n⏳ Час початку:\n{str(start_time).split('.')[0]}" \
                                F"\n⌛ Час завершення:\n{str(finish_time).split('.')[0]}" \
                                F"\n⏰ Витрачено часу: {str(finish_time - start_time).split('.')[0]}" \
                                F"\n🕐 Можлива тривалість: {str(user_test[9])} хвилин" \
                                F"\n📄 Оцінка: {str(user_test[2])}"
    await bot.edit_message_text(chat_id=event.from_user.id, message_id=event.message.message_id,text="🗂 Мої результати\n" + user_data_parsed_list, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="◀ Повернутися", callback_data="return_state")))


@dp.callback_query_handler(lambda msg: True, state=FSMResult.return_state)
async def result_view_handler(event: types.Message, state: FSMContext):
    await state.finish()
    await FSMResult.chooseResult.set()
    await bot.edit_message_text(chat_id=event.from_user.id, message_id=event.message.message_id, text="📑 Список результатів:",
                           reply_markup=init_user_test_button_list(event.from_user.id))
