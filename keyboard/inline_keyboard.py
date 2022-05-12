import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot_init import *
from datetime import datetime
import pytz

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


def getInlineTestListById(test_num, current_test_number):
    ans = InlineKeyboardMarkup(row_width=2)
    ans.inline_keyboard.clear()
    ans = InlineKeyboardMarkup(row_width=30)
    res = testRepo.findAllQuestionByTestId(test_num)
    btn = [[]]
    for val in res:
        if len(btn[len(btn) - 1]) == 7:
            btn.append([])
        if current_test_number == val[4]:
            text = '⏺' + str(val[4])
        else:
            text = str(val[4])
        btn[len(btn) - 1].append(InlineKeyboardButton(text=text, callback_data=F"testNumber_{val[4]}_{val[0]}"))

    for val in btn:
        ans.row(*val)
    return ans


def getTestData(test_id, q_num):
    ans = testRepo.findQuestionByTestIdAndQuestionNumber(test_id, q_num)
    return ans


def init_start_stop_test_keyboard(state):
    ans = InlineKeyboardMarkup(row_width=2)
    ans.inline_keyboard.clear()
    if state == 0:
        ans.add(InlineKeyboardButton(text="Розпочати тест", callback_data="Start"))
    else:
        ans.add(InlineKeyboardButton(text="Завершити тест", callback_data="Stop"))
    return ans


def init_user_test_button_list(user_id):
    user_test_list = testRepo.findAllUserTestByUserId(user_id)
    user_test_button_list = InlineKeyboardMarkup(row_width=100)
    user_test_button_list.inline_keyboard.clear()
    for test in user_test_list:
        test_name = testRepo.findTestByTestId(test[5])[2]
        test_timestamp = datetime.fromisoformat(str(test[3]))
        test_start_time = (str(test_timestamp).split(' ')[1].split('.')[0])
        test_start_date = str(test_timestamp).split(' ')[0]
        score = str(test[2])
        user_test_button_list.add(InlineKeyboardButton(text=F"{test_start_time} {test_start_date}:"
                                                            F"\n{test_name}"
                                                            F"\nОцінка: {score}", callback_data=F"testId_{test[0]}"))
    return user_test_button_list

