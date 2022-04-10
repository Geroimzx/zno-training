from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ---- Main menu ----
chooseYear = KeyboardButton('Вибір року')
typeOfSession = KeyboardButton('Тип сесії')
chooseSubject = KeyboardButton('Вибір предмету')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(chooseYear, typeOfSession,chooseSubject)

# ---- Main menu inline ----
chooseYear_inline = InlineKeyboardButton('Вибір року', callback_data='button1')
typeOfSession_inline = InlineKeyboardButton('Тип сесії', callback_data='button2')
chooseSubject_inline = InlineKeyboardButton('Вибір предмету', callback_data='button3')
mainMenu_inline = InlineKeyboardMarkup().add(chooseYear_inline, typeOfSession_inline, chooseSubject_inline)


