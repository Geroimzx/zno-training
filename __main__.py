import asyncio
import psycopg2

from aiogram import Bot, Dispatcher, executor, types
from config import *
from repository.UserRepository import UserRepository

try:
    # DB Connection
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    conn.autocommit = True
    print("[INFO] Connection opened")
except psycopg2.Error as e:
    print("[INFO] Connection failed".format(e))

# User Data Access Object
userDao = UserRepository(conn)


# Call when /start or /restart
async def start_handler(event: types.Message):
    # Test if user exist: if true - yes, false - no
    print("[DEBUG] User ", event.from_user.id, " is exists: ",
          userDao.existsUserById(event.from_user.id))

    # If User not exists in DB insert him data into DB
    if not userDao.existsUserById(event.from_user.id):
        userDao.addUser(user_id=event.from_user.id, user_name=event.from_user.username,
                        first_name=event.from_user.first_name, last_name=event.from_user.last_name)

    await event.answer(
        f"Привіт, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )


def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(start_handler, commands={"start", "restart"})
        executor.start_polling(disp)
    finally:
        conn.close()
        print("[INFO] Connection to DB closed")


if __name__ == '__main__':
    main()
