from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

import psycopg2

from config import *
from repository.repository_init import *


# Bot
bot = Bot(token=M_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


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