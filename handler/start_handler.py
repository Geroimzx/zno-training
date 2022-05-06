from aiogram import types

from bot_init import *

# ---- Tmp Buttons ----
import keyboard.keyboard as nav


# Call when /start or /restart
@dp.message_handler(commands={"start", "restart"})
async def start_handler(event: types.Message):
    # If User not exists in DB insert him data into DB
    if not userRepo.existsUserById(event.from_user.id):
        userRepo.addUser(user_id=event.from_user.id, user_name=event.from_user.username,
                         first_name=event.from_user.first_name, last_name=event.from_user.last_name)
    await event.answer(
        f"Привіт, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
        reply_markup=nav.keyboard,
    )


# Call when /test
@dp.message_handler(commands={"test"})
async def test_handler(event: types.Message):
    await event.answer(
        "[DEBUG] All subjects: " + str(testRepo.findAllSubject()) + "\nSubject id 1: " + str(
            testRepo.findSubjectById(1)) + "\nTest id 1 Question 1: " + str(
            testRepo.findQuestionByTestIdAndQuestionNumber(1, 1)),
        parse_mode=types.ParseMode.HTML
    )