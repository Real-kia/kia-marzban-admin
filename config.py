

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import json

file_path = 'config.json'

with open(file_path, 'r') as json_file:
    config_dict = json.load(json_file)

bot_token = config_dict['bot_token']

bot = Bot(bot_token, parse_mode=None)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

