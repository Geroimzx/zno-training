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

    await bot.edit_message_text(chat_id=event.from_user.id, message_id=event.message.message_id,
                                text=F'{testRepo.findSubjectById(event.data.split("_")[1])[0][0]}')

    from interface.menusButtons import createYearList
    msgText = "Доступні роки:\r\n"
    for val in createYearList(event.data.split('_')[1]):
        msgText += val + "\r\n"
    await bot.send_message(chat_id=event.from_user.id, text=msgText)
    await bot.send_message(chat_id=event.from_user.id, text="Введіть рік:")


async def choosed_year_handler(event: types.Message, state: FSMContext):
    from __main__ import bot, testRepo
    if not event.text.isdecimal():
        await bot.send_message(event.from_user.id, "Введіть число!!")
        return

    yearAvailable = False
    from interface.menusButtons import createYearList
    async with state.proxy() as data:
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
        return

    async with state.proxy() as data:
        data['Year'] = event.text
        res = testRepo.findAllTestBySubjectIdAndYear(data['subjId'], event.text)
    await FSMStartTest.next()

    inlineSubj = types.InlineKeyboardMarkup()
    inlineSubj.inline_keyboard.clear()
    for val in res:
        inlineSubj.add(types.InlineKeyboardButton(text=val[2]+F'({val[3]}min)', callback_data=F'testID_{val[0]}'))
    await bot.send_message(event.from_user.id, 'Виберіть тип тесту:', reply_markup=inlineSubj)


async def choosen_test_handler(event: types.Message, state: FSMContext):
    from __main__ import bot
    await FSMStartTest.next()
    await bot.send_message(event.from_user.id, event.data)


def register_handlers_main_menu(dp: Dispatcher):
    dp.register_message_handler(startTest_handler, lambda msg: msg.text == "📝 Вибір предмету", state=None)
    dp.register_callback_query_handler(choosed_subject_handler, lambda c: True,
                                       state=FSMStartTest.chooseSubject)
    dp.register_message_handler(choosed_year_handler, lambda msg: True, state=FSMStartTest.chooseYear)
    dp.register_callback_query_handler(choosen_test_handler, lambda msg: True, state=FSMStartTest.chooseTestType)
