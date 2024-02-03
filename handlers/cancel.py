from config import dp, bot
from keyboards.keybaords import startkeyboard
from aiogram.dispatcher import FSMContext
from aiogram import types

from handlers.template import new_template
from handlers.node import node_update, new_node
from handlers.cnofig_manage import new_config, new_config_template
def cancel_setup():


    @dp.callback_query_handler(text=["cancelask"],state=[new_template , node_update, new_node, new_config_template, new_config])
    async def cancel_ask(callback_query: types.CallbackQuery, state: FSMContext):
        await state.finish()
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, 
        text='لغو', reply_markup=startkeyboard)
