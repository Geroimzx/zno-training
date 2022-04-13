from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMStartTest(StatesGroup):
    chooseSubject = State()
    chooseYear = State()
    chooseTestType = State()
    startTest = State()
    endTest = State()


async def startTest_handler(message: types.Message):
    from __main__ import bot
    from interface.menusButtons import subj_menu, createSubjectMenu, return_menu
    await FSMStartTest.chooseSubject.set()
    createSubjectMenu()
    obj_message = await bot.send_message(message.from_user.id, 'Виберіть предмет:', reply_markup=subj_menu)


async def choosed_subject_handler(event: types.Message, state: FSMContext):
    from __main__ import bot, testRepo
    async with state.proxy() as data:
        data['msg'] = event
        data['subjId'] = event.data.split('_')[1]
    await FSMStartTest.next()
    async with state.proxy() as data:
        data['msg'] = await bot.edit_message_text(chat_id=event.from_user.id, message_id=event.message.message_id,
                                                  text=F'{testRepo.findSubjectById(event.data.split("_")[1])[0][0]}')
    from interface.menusButtons import createYearList
    msgText = "Доступні роки:\r\n"
    for val in createYearList(event.data.split('_')[1]):
        msgText += val + "\r\n"
    msg1 = await bot.send_message(chat_id=event.from_user.id, text=msgText)
    msg2 = await bot.send_message(chat_id=event.from_user.id, text="Введіть рік:")
    async with state.proxy() as data:
        data['msg1'] = msg1
        data['msg2'] = msg2


async def choosed_year_handler(event: types.Message, state: FSMContext):
    from __main__ import bot, testRepo
    if not event.text.isdecimal():
        async with state.proxy() as data:
            await bot.send_message(event.from_user.id, "Введіть число!!")
        await bot.delete_message(chat_id=event.from_user.id, message_id=event.message_id)
        return

    yearAvailable = False
    from interface.menusButtons import createYearList
    async with state.proxy() as data:
        data['user_msg'] = event
        for val in createYearList(data['subjId']):
            tmp = val.split('-')
            if len(tmp) > 1:
                if int(tmp[0]) <= int(event.text) <= int(tmp[1]):
                    yearAvailable = True
                    break
            elif int(event.text) == int(tmp[0]):
                yearAvailable = True
                break
    if not yearAvailable:
        await bot.send_message(event.from_user.id, "Введіть доступний рік!!")
        await bot.delete_message(chat_id=event.from_user.id, message_id=event.message_id)
        return

    async with state.proxy() as data:
        data['Year'] = event.text
        await bot.delete_message(chat_id=data['msg1'].chat.id, message_id=data['msg1'].message_id)
        await bot.delete_message(chat_id=data['msg2'].chat.id, message_id=data['msg2'].message_id)
        await bot.delete_message(chat_id=data['user_msg'].from_user.id,
                                 message_id=data['user_msg'].message_id)
        data.pop('msg1')
        data.pop('msg2')
        data.pop('user_msg')
        await bot.edit_message_text(chat_id=data['msg'].chat.id, message_id=data['msg'].message_id,
                                    text=data['msg'].text + F"\r\n{event.text}")
        res = testRepo.findAllTestBySubjectIdAndYear(data['subjId'], event.text)
    await FSMStartTest.next()

    inlineSubj = types.InlineKeyboardMarkup()
    inlineSubj.inline_keyboard.clear()
    for val in res:
        inlineSubj.add(types.InlineKeyboardButton(text=val[2]+F'({val[3]}min)',
                                                  callback_data=F'testID_{val[0]}_{val[3]}'))
    await bot.send_message(event.from_user.id, 'Виберіть тип тесту:', reply_markup=inlineSubj)


async def choosen_test_handler(event: types.Message, state: FSMContext):
    from __main__ import bot, testRepo
    await FSMStartTest.next()
    res = testRepo.findAllQuestionByTestId(event.data.split('_')[1])
    async with state.proxy() as data:
        data['Tests_data'] = res
        data['Time_test'] = event.data.split('_')[2]
    await bot.send_message(event.from_user.id, str(res))


def register_handlers_main_menu(dp: Dispatcher):
    dp.register_message_handler(startTest_handler, lambda msg: msg.text == "📝 Вибір предмету", state="*")
    dp.register_callback_query_handler(choosed_subject_handler, lambda c: True,
                                       state=FSMStartTest.chooseSubject)
    dp.register_message_handler(choosed_year_handler, lambda msg: True, state=FSMStartTest.chooseYear)
    dp.register_callback_query_handler(choosen_test_handler, lambda msg: True, state=FSMStartTest.chooseTestType)
