from config import dp, bot
from keyboards.keybaords import startkeyboard
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import os
import json
import requests
from aiogram.dispatcher.filters.state import State, StatesGroup


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.panel import get_templates, get_inbounds
from utils.config_create import bulk_config_create
from utils.login import login
from keyboards.keybaords import  cancel_menu, startkeyboard

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

config_path = os.path.join(parent_dir, 'config.json')

with open(config_path, 'r') as json_file:
    config_dict = json.load(json_file)

panel_username = config_dict['panel_username']
panel_pass = config_dict['panel_pass']
panel_address = config_dict['panel_address']
dev_version = config_dict['dev_version']


def config_setup():
    @dp.callback_query_handler(text=["config_create"])
    async def config_manage(callback_query: types.CallbackQuery, state: FSMContext):
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id
        template_list = get_templates()
        config_creation_mode_keybaord = InlineKeyboardMarkup()

        #no template rn
        if len(template_list) == 0:
            no_temp_btn = InlineKeyboardButton('شما تمپلیتی ندارید',callback_data='shit')
            add_template_btn = InlineKeyboardButton('افزودن تمپلیت جدید', callback_data='add_template')
            config_creation_mode_keybaord.add(no_temp_btn)
            config_creation_mode_keybaord.add(add_template_btn)
        else:
            for template in template_list:
                template_id = template['id']
                template_name_btn = InlineKeyboardButton(template['name'], callback_data=f'ConfigCreate_{template_id}')
                config_creation_mode_keybaord.add(template_name_btn)
        manual_config_create_btn = InlineKeyboardButton('ساخت کانفیگ به صورت دستی', callback_data='config_create_manual')
        config_creation_mode_keybaord.add(manual_config_create_btn)
        cancel_btn_inline =InlineKeyboardButton("لغو", callback_data='cancelask')
        config_creation_mode_keybaord.add(cancel_btn_inline)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"برای ساخت کانفیگ از روی تمپلیت کلیک کنید\nیا به صورت دستی کانفیگ بسازید\n(در صورت ساخت کانفیگ به صورت دستی تمام اینباند ها استفاده میشوند)", reply_markup=config_creation_mode_keybaord)


class new_config_template(StatesGroup):
    WaitingForName= State()
    WaitingForTedad = State()
def config_create_template_setup():
    @dp.callback_query_handler(lambda c: c.data.startswith('ConfigCreate_'))
    async def temp_config_create_(callback_query: types.CallbackQuery, state: FSMContext):
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.message_id

        template_id = callback_query.data[len('ConfigCreate_'):]
        await state.update_data(template_id = template_id)
        await new_config_template.WaitingForName.set()
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'اسم کانفیگ ها را با فرمت درست وارد کنید\nحداقل ۴ حرف باشد\nاز حروف انگلیسی و مجاز استفاده کنید\nدر کانفیگ های ساخته شده ابتدا اسم ورودی هست و بعدش یک عدد که از ۱ شروع میشود\nاگه در اخر اسم عدد باشد عدد ها از عدد بعد از ان شروع میشن', reply_markup=cancel_menu)
    @dp.message_handler(state=new_config_template.WaitingForName)
    async def proces_name(message: types.Message, state: FSMContext):


        name = message.text
        chat_id = message.chat.id

        await state.update_data(name=name)


        await bot.send_message(text='تعداد را وارد کنید' ,chat_id=chat_id, reply_markup=cancel_menu)

        await new_config_template.WaitingForTedad.set()
    @dp.message_handler(state=new_config_template.WaitingForTedad)
    async def proces_tedad(message: types.Message, state: FSMContext):


        tedad = message.text
        chat_id = message.chat.id

        data = await state.get_data()
        await state.finish()
        name = data['name']
        await bot.send_message(text=f'در حال ساخت...\nدر صورتی که تعداد بالا باشد نیاز به زمان هست' ,chat_id=chat_id)
        token = login(panel_username, panel_pass)
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}',
        }
        template_id = data['template_id']
        response = requests.get(f'{panel_address}api/user_template/{template_id}', headers=headers)
        template = json.loads(response.text)
        days = template['expire_duration']
        hajm = template['data_limit']
        inbounds = template['inbounds']
        sub_links = bulk_config_create(name = name, hajm=hajm, days=days, tedad=tedad, inbounds=inbounds, token=token)
        for sub_link in sub_links:
            if dev_version == True:
                await bot.send_message(chat_id=chat_id, text=sub_link)
            else:
                await message.reply(f"{panel_address[:-1]}{sub_link}")

        await bot.send_message(chat_id=chat_id, text='پایان', reply_markup=startkeyboard)

class new_config(StatesGroup):
    WaitingForName= State()
    WaitingForTedad = State()
    WaitingForHajm = State()
    WaitingForDay = State()

def config_create_manual_setup():
    @dp.callback_query_handler(text=["config_create_manual"])
    async def ask_msg(callback_query: types.CallbackQuery, state: FSMContext):
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id



        # Edit the message text
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'اسم کانفیگ ها را با فرمت درست وارد کنید\nحداقل ۴ حرف باشد\nاز حروف انگلیسی و مجاز استفاده کنید\nدر کانفیگ های ساخته شده ابتدا اسم ورودی هست و بعدش یک عدد که از ۱ شروع میشود\nاگه در اخر اسم عدد باشد عدد ها از عدد بعد از ان شروع میشن', reply_markup=cancel_menu)

        await new_config.WaitingForName.set()



    @dp.message_handler(state=new_config.WaitingForName)
    async def proces_name(message: types.Message, state: FSMContext):


        name = message.text
        chat_id = message.chat.id

        await state.update_data(name=name)


        await bot.send_message(text='تعداد را وارد کنید' ,chat_id=chat_id, reply_markup=cancel_menu)

        await new_config.WaitingForTedad.set()

    @dp.message_handler(state=new_config.WaitingForTedad)
    async def proces_name(message: types.Message, state: FSMContext):


        tedad = message.text
        chat_id = message.chat.id

        await state.update_data(tedad=tedad)


        await bot.send_message(text='حجم را وارد کنید' ,chat_id=chat_id, reply_markup=cancel_menu)

        await new_config.WaitingForHajm.set()

    @dp.message_handler(state=new_config.WaitingForHajm)
    async def proces_hajm(message: types.Message, state: FSMContext):


        hajm = message.text
        chat_id = message.chat.id

        await state.update_data(hajm=hajm)


        await bot.send_message(text='روز را وارد کنید' ,chat_id=chat_id, reply_markup=cancel_menu)

        await new_config.WaitingForDay.set()



    @dp.message_handler(state=new_config.WaitingForDay)
    async def proces_day(message: types.Message, state: FSMContext):


        day = message.text
        chat_id = message.chat.id

        await state.update_data(day=day)
        data = await state.get_data()
        await state.finish()
        await message.reply(data)


        token = login(panel_username, panel_pass)
        
        inbounds = get_inbounds()
        inbounds_vless = inbounds['vless']
        vl_inbound_tags = []
        for inbound in inbounds_vless:
            vl_inbound_tags.append(inbound['tag'])
        inbounds_vmess = inbounds['vmess']
        vm_inbound_tags = []
        for inbound in inbounds_vmess:
            vm_inbound_tags.append(inbound['tag'])
        inbounds = {'vmess': vm_inbound_tags, "vless":vl_inbound_tags}
        sub_links = bulk_config_create(name=data['name'], hajm=data['hajm'], days=data['day'], tedad=data['tedad'],inbounds=inbounds,token=token)



        for sub_link in sub_links:
            if dev_version == True:
                await message.reply(f"{sub_link}")
            else:
                await message.reply(f"{panel_address[:-1]}{sub_link}")

        await message.reply('انجام شد', reply_markup=startkeyboard)

