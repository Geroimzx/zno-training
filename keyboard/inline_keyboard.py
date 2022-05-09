from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_init import *

subject_inline_button_array = []
year_array = []


def init_subject_inline_menu():
    subject_data_array = testRepo.findAllSubject()
    subject_inline_button_array.clear()
    for subject_data in subject_data_array:
        subject_inline_button_array.append(
            InlineKeyboardButton(text=F"{subject_data[0]}", callback_data=F"subject_{subject_data[1]}"))
    subject_menu = InlineKeyboardMarkup(row_width=3)
    subject_menu.inline_keyboard.clear()
    subject_menu.add(*subject_inline_button_array)
    return subject_menu


def init_year_array(subject_id):
    year_data_array = testRepo.findAllYearBySubjectId(subject_id)
    year_array.clear()
    for year_data in year_data_array:
        year_array.append(int(year_data[1]))


def init_year_inline_button(subject_id):
    init_year_array(subject_id)
    year_inline_button_array = InlineKeyboardMarkup()
    year_inline_button_array.inline_keyboard.clear()
    btn = [[]]
    for val in year_array:
        if len(btn[len(btn) - 1]) == 3:
            btn.append([])
        btn[len(btn) - 1].append(InlineKeyboardButton(text=F"{val}", callback_data=F"testYear_{val}"))
    for val in btn:
        year_inline_button_array.row(*val)
    return year_inline_button_array


def getInlineTestListById(test_id, current_test_number):
    ans = InlineKeyboardMarkup(row_width=2)
    ans.inline_keyboard.clear()
    ans = InlineKeyboardMarkup(row_width=30)
    res = testRepo.findAllQuestionByTestId(test_id)
    btn = [[]]
    for val in res:
        if len(btn[len(btn) - 1]) == 7:
            btn.append([])
        if current_test_number == val[4]:
            text = '⏺' + str(val[4])
        else:
            text = str(val[4])
        btn[len(btn) - 1].append(InlineKeyboardButton(text=text, callback_data=F"testNumber_{val[4]}"))

    for val in btn:
        ans.row(*val)
    return ans


def getTestData(test_id, q_num):
    ans = testRepo.findQuestionByTestIdAndQuestionNumber(test_id, q_num)
    return ans
