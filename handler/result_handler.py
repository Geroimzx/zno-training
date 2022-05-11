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
        data['user_test_name'] = testRepo.findTestByTestId(event.data.split("_")[1])
    await FSMResult.next()
    async with state.proxy() as data:
        user_test = testRepo.findUserTestWithTestNameByUserTestId(event.data.split("_")[1])
        user_data_parsed_list = F"\nНазва тесту:\n{str(user_test[8])}" \
                                F"\nЧас початку:\n{str(user_test[3])}" \
                                F"\nЧас завершення:\n{str(user_test[4])}" \
                                F"\nВитрачено часу: {str(user_test[4] - user_test[3]).split('.')[0]}" \
                                F"\nОцінка: {str(user_test[2])}"
    await bot.send_message(event.from_user.id, '🗂 Мої результати\n' + user_data_parsed_list)