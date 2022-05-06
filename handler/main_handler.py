from aiogram import types
from aiogram.dispatcher import FSMContext

from state.FSMStartTest import *
from keyboard.inline_keyboard import *

from bot_init import *


@dp.message_handler(lambda msg: msg.text == "📝 Вибір предмету", state="*")
async def subject_handler(message: types.Message):
    from keyboard.inline_keyboard import subj_menu, createSubjectMenu
    await FSMStartTest.chooseSubject.set()
    createSubjectMenu()
    obj_message = await bot.send_message(message.from_user.id, 'Виберіть предмет:', reply_markup=subj_menu)


@dp.callback_query_handler(lambda c: True, state=FSMStartTest.chooseSubject)
async def year_handler(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = event
        data['subjId'] = event.data.split('_')[1]
    await FSMStartTest.next()
    async with state.proxy() as data:
        data['msg'] = await bot.edit_message_text(chat_id=event.from_user.id, message_id=event.message.message_id,
                                                  text=F'{testRepo.findSubjectById(event.data.split("_")[1])[0][0]}')
    msg1 = await bot.send_message(chat_id=event.from_user.id, text="Виберіть рік:",
                                  reply_markup=createYearInlineList(event.data.split('_')[1]))
    print(msg1)
    async with state.proxy() as data:
        data['msg2'] = msg1


@dp.callback_query_handler(lambda msg: True, state=FSMStartTest.chooseYear)
async def test_type_handler(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Year'] = event.data.split('_')[1]

        await bot.delete_message(chat_id=data['msg2'].chat.id, message_id=data['msg2'].message_id)

        data.pop('msg2')

        data['msg'] = await bot.edit_message_text(chat_id=data['msg'].chat.id, message_id=data['msg'].message_id,
                                                  text=data['msg'].text + F"\r\n{event.data.split('_')[1]}")

        res = testRepo.findAllTestBySubjectIdAndYear(data['subjId'], event.data.split('_')[1])
    await FSMStartTest.next()

    inlineSubj = types.InlineKeyboardMarkup()
    inlineSubj.inline_keyboard.clear()
    for val in res:
        inlineSubj.add(types.InlineKeyboardButton(text=val[2] + F'({val[3]}min)',
                                                  callback_data=F'testID_{val[0]}_{val[3]}'))
    async with state.proxy() as data:
        data['msg1'] = await bot.send_message(event.from_user.id, 'Виберіть тип тесту:', reply_markup=inlineSubj)


@dp.callback_query_handler(lambda msg: True, state=FSMStartTest.startTest)
async def question_choose_handler(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg = getTestData(data['Test_id'], event.data.split('_')[1])

        data['Test_msg'] = await bot.edit_message_text(chat_id=data['Test_msg'].chat.id,
                                                       message_id=data['Test_msg'].message_id,
                                                       text=F"Питання {msg[0][4]}. \r\n{msg[0][2]}",
                                                       reply_markup=getInlineTestListById(data['Test_id']))
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
                                                          text=data['msg'].text + F"\r\n{var[0].text}")
                await bot.delete_message(chat_id=data['msg1'].chat.id, message_id=data['msg1'].message_id)
                data.pop('msg1')
                break

        msg = getTestData(data['Test_id'], event.data.split('_')[1])

        data['Test_msg'] = await bot.send_message(chat_id=event.from_user.id,
                                                  text=F"Питання {msg[0][4]}. \r\n{msg[0][2]}",
                                                  reply_markup=getInlineTestListById(data['Test_id']))
        if msg[0][3] != '':
            data['media_msg'] = await bot.send_photo(chat_id=data['Test_msg'].chat.id,
                                                     caption=F'To {data["Test_id"]}',
                                                     photo=msg[0][3])



