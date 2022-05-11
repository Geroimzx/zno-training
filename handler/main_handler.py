from aiogram import types
from aiogram.dispatcher import FSMContext

from state.FSMStartTest import *
from keyboard.inline_keyboard import *

from bot_init import *

from datetime import datetime
import pytz


@dp.message_handler(lambda msg: msg.text == "📝 Вибір предмету", state="*")
async def subject_handler(message: types.Message):
    from keyboard.inline_keyboard import init_subject_inline_menu
    await FSMStartTest.chooseSubject.set()
    await bot.send_message(message.from_user.id, 'Виберіть предмет:', reply_markup=init_subject_inline_menu())


@dp.callback_query_handler(lambda c: True, state=FSMStartTest.chooseSubject)
async def year_handler(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = event
        data['subjectId'] = event.data.split('_')[1]
    await FSMStartTest.next()
    async with state.proxy() as data:
        data['msg'] = await bot.edit_message_text(chat_id=event.from_user.id, message_id=event.message.message_id,
                                                  text=F'{testRepo.findSubjectById(event.data.split("_")[1])[0][0]}')
    enter_year_button = await bot.send_message(chat_id=event.from_user.id, text="Виберіть рік:",
                                               reply_markup=init_year_inline_button(event.data.split('_')[1]))
    async with state.proxy() as data:
        data['enter_year_message'] = enter_year_button


@dp.callback_query_handler(lambda msg: True, state=FSMStartTest.chooseYear)
async def test_type_handler(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Year'] = event.data.split('_')[1]

        await bot.delete_message(chat_id=data['enter_year_message'].chat.id,
                                 message_id=data['enter_year_message'].message_id)
        data.pop('enter_year_message')

        data['msg'] = await bot.edit_message_text(chat_id=data['msg'].chat.id, message_id=data['msg'].message_id,
                                                  text=data['msg'].text + F"\r\n{event.data.split('_')[1]}")

        res = testRepo.findAllTestBySubjectIdAndYear(data['subjectId'], event.data.split('_')[1])
    await FSMStartTest.next()

    inline_subj = types.InlineKeyboardMarkup()
    inline_subj.inline_keyboard.clear()
    for val in res:
        inline_subj.add(types.InlineKeyboardButton(text=val[2] + F'({val[3]}хв)',
                                                   callback_data=F'testID_{val[0]}_{val[3]}'))
    async with state.proxy() as data:
        data['msg1'] = await bot.send_message(event.from_user.id, 'Виберіть тип тесту:', reply_markup=inline_subj)


@dp.callback_query_handler(lambda msg: True, state=FSMStartTest.chooseTestType)
async def test_question_handler(event: types.Message, state: FSMContext):
    await FSMStartTest.next()

    res = testRepo.findAllQuestionByTestId(event.data.split('_')[1])

    async with state.proxy() as data:
        data['Test_id'] = event.data.split('_')[1]
        data['Tests_data'] = res
        data['Time_test'] = event.data.split('_')[2]

        for var in event.message.reply_markup.inline_keyboard:
            if var[0].callback_data == event.data:
                data['msg'] = await bot.edit_message_text(chat_id=data['msg'].chat.id,
                                                          message_id=data['msg'].message_id,
                                                          text="🔖" + data['msg'].text + F"\r\n📄{var[0].text}",
                                                          reply_markup=init_start_stop_test_keyboard(0))

                await bot.delete_message(chat_id=data['msg1'].chat.id, message_id=data['msg1'].message_id)
                data.pop('msg1')
                break


@dp.callback_query_handler(lambda msg: msg.data == 'Start', state=FSMStartTest.waitForUser)
async def start_test_handler(event: types.Message, state: FSMContext):
    await FSMStartTest.next()

    async with state.proxy() as data:
        data['msg'] = await bot.edit_message_reply_markup(chat_id=data['msg'].chat.id,
                                                          message_id=data['msg'].message_id,
                                                          reply_markup=init_start_stop_test_keyboard(1))
        msg = getTestData(data['Test_id'], 1)
        data['Test_msg'] = await bot.send_message(chat_id=event.from_user.id,
                                                  text=F"Питання {msg[0][4]}. \r\n{msg[0][2]}",
                                                  reply_markup=getInlineTestListById(data['Test_id'], 1))
        if msg[0][3] != '':
            data['media_msg'] = await bot.send_photo(chat_id=data['Test_msg'].chat.id,
                                                     photo=msg[0][3],
                                                     caption='До 1 завдання')

        tz_UA = pytz.timezone('Europe/Kiev')
        data['Start_time'] = datetime.now(tz_UA)
        data['Record_user_test_id'] = testRepo.createUserTest(event.from_user.id, data['Test_id'], data['Start_time'])


# Finish test state
@dp.callback_query_handler(lambda msg: msg.data == "Stop", state=FSMStartTest.startTest)
async def question_choose_handler(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'Test_msg' in data.keys():
            await bot.delete_message(chat_id=data['Test_msg'].chat.id,
                                     message_id=data['Test_msg'].message_id)
            data.pop('Test_msg')
        if 'media_msg' in data.keys():
            await bot.delete_message(chat_id=data['media_msg'].chat.id,
                                     message_id=data['media_msg'].message_id)
            data.pop('media_msg')
        await bot.edit_message_reply_markup(chat_id=data['msg'].chat.id,
                                            message_id=data['msg'].message_id,
                                            reply_markup=InlineKeyboardMarkup().inline_keyboard.clear())

        tz_UA = pytz.timezone('Europe/Kiev')
        data['End_time'] = datetime.now(tz_UA)
        data['msg'] = await bot.edit_message_text(chat_id=data['msg'].chat.id,
                                                  message_id=data['msg'].message_id,
                                                  text=data['msg'].text + F"\r\nЧас початку:"
                                                                          F"\r\n{str(data['Start_time']).split('.')[0]}"
                                                                          F"\r\nЧас завершення:"
                                                                          F"\r\n{str(data['End_time']).split('.')[0]}"
                                                                          F"\r\nВитрачено часу: "
                                                                          F"{str(data['End_time'] - data['Start_time']).split('.')[0]} "
                                                                          F"\r\nScore: tratata")
        testRepo.updateUserTestFinished(data['Record_user_test_id'], data['End_time'])
    await event.answer(text="Тест успішно завершений")
    await state.finish()


@dp.callback_query_handler(lambda msg: True, state=FSMStartTest.startTest)
async def question_choose_handler(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg = getTestData(data['Test_id'], event.data.split('_')[1])

        data['Test_msg'] = await bot.edit_message_text(chat_id=data['Test_msg'].chat.id,
                                                       message_id=data['Test_msg'].message_id,
                                                       text=F"Питання {msg[0][4]}. \r\n{msg[0][2]}",
                                                       reply_markup=getInlineTestListById(data['Test_id'], msg[0][4]))
        if msg[0][3] != '':
            if 'media_msg' in data.keys():
                await bot.delete_message(chat_id=data['media_msg'].chat.id,
                                         message_id=data['media_msg'].message_id)
            data['media_msg'] = await bot.send_photo(chat_id=data['Test_msg'].chat.id,
                                                     caption=F'До {event.data.split("_")[1]} завдання',
                                                     photo=msg[0][3])
        else:
            if 'media_msg' in data.keys():
                await bot.delete_message(chat_id=data['media_msg'].chat.id,
                                         message_id=data['media_msg'].message_id)
                data.pop('media_msg')


@dp.message_handler(lambda msg: msg.text == '❌ Скасувати', state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await message.answer('✅', reply=True)
