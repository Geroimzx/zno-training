from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Reply main menu
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
# Buttons
keyboard_buttons = ["📝 Вибір предмету", "🗂 Мої результати", "❌ Скасувати", "📈 Статистика"]
keyboard.add(*keyboard_buttons)

# Return to menu button
return_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(" Повернутися"))
