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
    from interface.menusButtons import subj_menu, createSubjectMenu
    await FSMStartTest.chooseSubject.set()
    createSubjectMenu()
    obj_message = await bot.send_message(message.from_user.id, 'Виберіть предмет:', reply_markup=subj_menu)


async def chooseYear_handler(event: types.Message, state: FSMContext):
    from __main__ import bot
    async with state.proxy() as data:
        data['msg'] = event
        data['subjId'] = event.data.split('_')[1]
    print(event)
    await FSMStartTest.next()
    await bot.edit_message_text(chat_id=event.from_user.id, message_id=event.message.message_id, text='Виберіть рік:')


def register_handlers_main_menu(dp: Dispatcher):
    dp.register_message_handler(startTest_handler, lambda msg: msg.text == "📝 Почати тест", state=None)
    dp.register_callback_query_handler(chooseYear_handler, lambda c: True,
                                       state=FSMStartTest.chooseSubject)
