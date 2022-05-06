from aiogram import types

from bot_init import *

from keyboard.keyboard import keyboard


# Call when /start or /restart
@dp.message_handler(commands={"start", "restart"})
async def start_handler(event: types.Message):
    # If User not exists in DB insert him data into DB
    if not userRepo.existsUserById(event.from_user.id):
        userRepo.addUser(user_id=event.from_user.id, user_name=event.from_user.username,
                         first_name=event.from_user.first_name, last_name=event.from_user.last_name)
    await event.answer(
        f"Привіт, {event.from_user.get_mention(as_html=True)} 👋!\n\n"
        f"Тут ти можеш пройти тестування ЗНО з:\n\n"
        f"📐 Математики\n"
        f"🧲 Фізики\n"
        f"🇺🇦 Української мови\n"
        f"📘📙 Української мови і літератури\n"
        f"📔 Історії України\n"
        f"🗺 Географії\n"
        f"🦠 Біології\n"
        f"🧪 Хімії\n"
        f"🇬🇧 Англійської мови\n\n"
        f"📎 Просто обери  в меню нижче 📝 Вибір предмету\n"
        f"📎 Твої результати будуть збережені в 🗂 Мої результати\n\n"
        f"🧾📈 Успіхів тобі!",
        parse_mode=types.ParseMode.HTML,
        reply_markup=keyboard,
    )