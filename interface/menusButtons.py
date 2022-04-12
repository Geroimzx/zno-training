from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Reply main menu
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
# Buttons
mm_buttons = ["📝 Почати тест", "🗂 Мої результати"]
main_menu.add(*mm_buttons)

subj_buttons = []
subj_menu = InlineKeyboardMarkup(row_width=3)

year_array = []


def createSubjectMenu():
    from __main__ import testRepo
    res = testRepo.findAllSubject()
    subj_buttons.clear()
    for val in res:
        subj_buttons.append(InlineKeyboardButton(text=F"{val[0]}", callback_data=F"subject_{val[1]}"))
    subj_menu.inline_keyboard.clear()
    subj_menu.add(*subj_buttons)


def createYearArr(subj_id):
    from __main__ import testRepo
    res = testRepo.findAllYearBySubjectId(subj_id)
    year_array.clear()
    prev = -1
    for val in res:
        if prev == -1:
            prev = int(val[1])
            continue
        if val - prev > 1:
            year_array.append(prev)
        prev = val
    year_array.append(prev)


def createYearList(subj_id):
    createYearArr(subj_id)
    list = []

    index = 0
    startIndex = 0
    for val in year_array:
        if index == 0:
            index += 1
            continue
        if year_array[index] - year_array[index - 1] > 1:
            if index - 1 - startIndex > 0:
                list.append(F'{year_array[startIndex]}-{year_array[index - 1]}')
                startIndex = index
            else:
                list.append(F'{year_array[index - 1]}')
                startIndex = index
        index += 1

    if index - 1 - startIndex > 0:
        list.append(F'{year_array[startIndex]}-{year_array[index - 1]}')
    else:
        list.append(F'{year_array[index - 1]}')

    return list



# ---- Main menu ----
# chooseYear = KeyboardButton('Вибір року')
# typeOfSession = KeyboardButton('Тип сесії')
# chooseSubject = KeyboardButton('Вибір предмету')
# mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(chooseYear, typeOfSession,chooseSubject)

# ---- Main menu inline ----
# chooseYear_inline = InlineKeyboardButton('Вибір року', callback_data='button1')
# typeOfSession_inline = InlineKeyboardButton('Тип сесії', callback_data='button2')
# chooseSubject_inline = InlineKeyboardButton('Вибір предмету', callback_data='button3')
# mainMenu_inline = InlineKeyboardMarkup().add(chooseYear_inline, typeOfSession_inline, chooseSubject_inline)
