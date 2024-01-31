from config import dp, bot
from keyboards.keybaords import startkeyboard
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import os
import json

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

config_path = os.path.join(parent_dir, 'config.json')

with open(config_path, 'r') as json_file:
    config_dict = json.load(json_file)

admin_chat_id = config_dict['admin_chat_id']

def start_setup():
    @dp.message_handler(Text(equals=['/start']))
    async def welcom(message: types.Message):
        if message.chat.id == admin_chat_id:
            await message.reply('خوش امدید', reply_markup=startkeyboard)
        else:
            print('not admin')

    @dp.callback_query_handler(text=["main_menu"])
    async def main_menu(callback_query: types.CallbackQuery, state: FSMContext):
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id


        # Edit the message text
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="منو اصلی", reply_markup=startkeyboard)




