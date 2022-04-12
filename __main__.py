import asyncio
import psycopg2

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *
from repository.UserRepository import *
from repository.TestRepository import *
from repository.SubjectRepository import *

from interface.menusCallbackAnswers import *

# ---- Tmp Buttons ----
import interface.menusButtons as nav

try:
    # DB Connection
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    conn.autocommit = True
    print("[INFO] Connection opened")
except psycopg2.Error as e:
    print("[INFO] Connection failed".format(e))

# User Repo DB
userRepo = UserRepository(conn)

# Test Repo DB
testRepo = TestRepository(conn)

# Subject Repo DB
subjectRepo = SubjectRepository(conn)

# Bot
bot = Bot(token=BOT_TOKEN_Max)
storage = MemoryStorage()


# Call when /start or /restart
async def start_handler(event: types.Message):
    # Test if user exist: if true - yes, false - no
    print("[DEBUG] User ", event.from_user.id, " is exists: ",
          userRepo.existsUserById(event.from_user.id))
#    print(userRepo.findAllUsers())
    # If User not exists in DB insert him data into DB
    if not userRepo.existsUserById(event.from_user.id):
        userRepo.addUser(user_id=event.from_user.id, user_name=event.from_user.username,
                         first_name=event.from_user.first_name, last_name=event.from_user.last_name)
    await event.answer(
        f"Привіт, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
        reply_markup=nav.main_menu,
    )


# Call when /test
async def test_handler(event: types.Message):
    await event.answer(
        "[DEBUG] All subjects: " + str(testRepo.findAllSubject()) + "\nSubject id 1: " + str(
            testRepo.findSubjectById(1)) + "\nTest id 1 Question 1: " + str(
            testRepo.findQuestionByTestIdAndQuestionNumber(1, 1)),
        parse_mode=types.ParseMode.HTML
    )


# ---- Main func ----
def main():
    try:
        dp = Dispatcher(bot=bot, storage=storage)
        dp.register_message_handler(start_handler, commands={"start", "restart"})
        dp.register_message_handler(test_handler, commands={"test"})
        #       ---- My test handlers ----
        register_handlers_main_menu(dp)
        #        dp.register_message_handler(test_handler2, lambda msg: msg.text == 'Вибір року')
        #        dp.register_callback_query_handler(test_handler2, lambda c: c.data == 'button1')

        executor.start_polling(dp)
    finally:
        conn.close()
        print("[INFO] Connection to DB closed")


if __name__ == '__main__':
    main()
