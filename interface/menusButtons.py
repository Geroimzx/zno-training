from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Reply main menu
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
# Buttons
mm_buttons = ["📝 Вибір предмету", "🗂 Мої результати"]
main_menu.add(*mm_buttons)

# Return to menu button
return_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("◀️Повернутися"))

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
            year_array.append(prev)
            continue

        if int(val[1]) - int(prev) > int(1):
            year_array.append(prev)
        prev = int(val[1])
    if prev > 1:
        year_array.append(prev)


def createYearList(subj_id):
    createYearArr(subj_id)
    listYears = []

    index = 0
    startIndex = 0
    for val in year_array:
        if index == 0:
            index += 1
            continue
        if year_array[index] - year_array[index - 1] > 1:
            if index - 1 - startIndex > 0:
                listYears.append(F'{year_array[startIndex]}-{year_array[index - 1]}')
                startIndex = index
            else:
                listYears.append(F'{year_array[index - 1]}')
                startIndex = index
        index += 1

    if index - 1 - startIndex > 0:
        listYears.append(F'{year_array[startIndex]}-{year_array[index - 1]}')
    else:
        listYears.append(F'{year_array[index - 1]}')

    return listYears

