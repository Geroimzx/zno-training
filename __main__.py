from aiogram.utils.executor import start_polling

from bot_init import dp, conn

from handler.start_handler import *
from handler.main_handler import *
from handler.result_handler import  *



# ---- Main func ----
def main():
    try:
        start_polling(dp, skip_updates=True)
    finally:
        conn.close()
        print("[INFO] Connection to DB closed")


if __name__ == '__main__':
    main()
