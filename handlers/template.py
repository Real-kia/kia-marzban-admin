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
from utils.login import login
from keyboards.keybaords import config_keyboard, cancel_menu






current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

config_path = os.path.join(parent_dir, 'config.json')

with open(config_path, 'r') as json_file:
    config_dict = json.load(json_file)

panel_username = config_dict['panel_username']
panel_pass = config_dict['panel_pass']
panel_address = config_dict['panel_address']





def template_setup():

    @dp.callback_query_handler(text=["manage_config"])
    async def config_menu(callback_query: types.CallbackQuery, state: FSMContext):
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="گزینه مورد نظر را انتخاب کنید", reply_markup=config_keyboard)



    #template menu 
    @dp.callback_query_handler(text=["manage_template"])
    async def template_manage(callback_query: types.CallbackQuery, state: FSMContext):
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id

        #getting template lists
        template_list = get_templates()
        templates_keyboard = InlineKeyboardMarkup()
        if len(template_list) > 0:

        
            
            name_btn = InlineKeyboardButton('اسم',callback_data='shit')
            days_btn = InlineKeyboardButton('روز', callback_data='shit')
            data_btn = InlineKeyboardButton('حجم', callback_data='shit')
            templates_keyboard.add(name_btn, days_btn, data_btn)
        else: 
            no_template_btn = InlineKeyboardButton('تمپلیتی ندارید برای ساخت اقدام کنید👇👇', callback_data='shit')
            templates_keyboard.add(no_template_btn)
        #adding templats to template keybaord
        for template in template_list:
            template_name_btn = InlineKeyboardButton(template['name'], callback_data='shit')
            days = str(int(template['expire_duration']))
            template_day_btn = InlineKeyboardButton(str(days), callback_data='shit')
            data = str(template['data_limit'])
            template_data_btn = InlineKeyboardButton(str(data), callback_data='shit')
            template_id = template['id']
            remove_template_btn = InlineKeyboardButton('حذف تمپلیت بالا', callback_data=f'templateRemove_{template_id}')        
            templates_keyboard.add(template_name_btn, template_day_btn, template_data_btn).add(remove_template_btn)
        
        
        
        add_template_btn = InlineKeyboardButton('افزودن تمپلیت جدید', callback_data='add_template')
        templates_keyboard.add(add_template_btn)
        
        
        config_manage_btn = InlineKeyboardButton('بازگشت', callback_data='manage_config')
        templates_keyboard.add(config_manage_btn)
        # Edit the message text
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="گزینه مورد نظر را انتخاب کنید", reply_markup=templates_keyboard)

def template_remove_setup():

    #template remove 
    @dp.callback_query_handler(lambda c: c.data.startswith('templateRemove_'))
    async def remove_template(callback_query: types.CallbackQuery):
        template_id = int(callback_query.data.split('_')[1])

        token = login(panel_username, panel_pass)
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}',
        }
        response = requests.delete(f'{panel_address}api/user_template/{template_id}', headers=headers)
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="با موفقیت حذف شد", reply_markup=startkeyboard)




#template add
class new_template(StatesGroup):
    WaitingForName= State()
    WaitingForDays = State()
    WaitingForData = State()
    WaitingForVless = State()
    WaitingForVmess = State()


def template_add_setup():



    @dp.callback_query_handler(text=["add_template"])
    async def aks_name(callback_query: types.CallbackQuery, state: FSMContext):
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id


        # Edit the message text
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="اسم را وارد کنید", reply_markup=cancel_menu)

        await new_template.WaitingForName.set()
    @dp.message_handler(state=new_template.WaitingForName)
    async def ask_template_days(message: types.Message, state: FSMContext):


        name = message.text
        await state.update_data(name=name)
        await message.reply(text='روز را به عدد وارد کنید', reply_markup=cancel_menu)

        await new_template.WaitingForDays.set()


    @dp.message_handler(state=new_template.WaitingForDays)
    async def ask_template_data(message: types.Message, state: FSMContext):


        days = message.text
        await state.update_data(days=days)
        await message.reply(text='حجم را به عدد وارد کنید', reply_markup=cancel_menu)

        await new_template.WaitingForData.set()


    @dp.message_handler(state=new_template.WaitingForData)
    async def template_inbound_ask(message: types.Message, state: FSMContext):
        hajm = message.text
        chat_id = message.chat.id

        await state.update_data(hajm=hajm)
        infos = await state.get_data()
        await state.finish()
        await new_template.WaitingForVless.set()
        await state.update_data(infos=infos)
        msg = await message.reply('در حال بارگیری' )
        msg_id = msg.message_id
        await update_inbound_keyboard(message_id=msg_id,chat_id=chat_id,protocol='Vless', state=state)
        






    @dp.callback_query_handler(lambda c: c.data == 'done', state=[new_template.WaitingForVless,new_template.WaitingForVmess])
    async def process_done(callback_query: types.CallbackQuery, state: FSMContext):


        chat_id = callback_query.message.chat.id

        data = await state.get_data()
        #with vmess
        vmess = False
        if 'vless' in data:
            vmess = True
            new_data = {'infos' : data['infos'], "vless":data['vless']}
            data.pop('infos')
            data.pop('vless')
            vmess_inbouns = []
            for vmess_inbound in data:
                vmess_inbouns.append(vmess_inbound)
            new_data['vmess'] = vmess_inbouns
        #no vless
        else:
            new_data = {'infos': data['infos']}
            data.pop('infos')
            vless_inbouns = []
            for vless_inbound in data:
                vless_inbouns.append(vless_inbound)
            new_data["vless"]=vless_inbouns    
            
        data = {"name":new_data['infos']['name'],"data_limit":new_data['infos']['hajm'],"expire_duration":new_data['infos']['days'], "inbounds":{"vless":new_data['vless']}}
        if vmess == True:
            
            data['inbounds']['vmess'] = new_data['vmess']
        await state.finish()
        
        token = login(panel_username, panel_pass)
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}',
        }

        # Send a response to the user or proceed with the next step in your logic
        await callback_query.answer('کانفیگ با موفقیت ثبت شد')
        response = requests.post(f'{panel_address}api/user_template', headers=headers, json=data)
        print(response.text)

        await bot.edit_message_text(chat_id=chat_id, message_id=callback_query.message.message_id, text='تمپلیت با موفقیت ثبت شد', reply_markup=startkeyboard)



    async def update_inbound_keyboard(message_id,chat_id, protocol,state : FSMContext):
        print('update inbound')
        inbound_keyboard = InlineKeyboardMarkup()

        inbounds = get_inbounds()
        type_lower = protocol.lower()

        for inbound in inbounds[type_lower]:
            inbound_name = inbound['tag']

            # Use different emoji based on the selection state
            is_selected = (await state.get_data()).get(inbound_name, False)
            emoji = '❌' if not is_selected else '✅'

            inbound_name_btn = InlineKeyboardButton(f'{emoji} {inbound_name}', callback_data=f'Select{type_lower}_{inbound_name}')
            inbound_keyboard.add(inbound_name_btn)
        if protocol == 'Vless':
            vmess_btn = InlineKeyboardButton('انتخاب کانفیگ های ویمس',callback_data='vmess_inbound')
            inbound_keyboard.add(vmess_btn)

        done_btn = InlineKeyboardButton('done✅', callback_data='done')
        inbound_keyboard.add(done_btn)
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="گزینه مورد نظر را انتخاب کنید", reply_markup=inbound_keyboard)

    @dp.callback_query_handler(lambda c: c.data == 'vmess_inbound', state=new_template.WaitingForVless)
    async def process_vmess(callback_query: types.CallbackQuery, state: FSMContext):
        chat_id = callback_query.message.chat.id

        data = await state.get_data()

        new_data = {'infos': data['infos']}
        data.pop('infos')
        vless_inbouns = []
        for vless_inbound in data:
            vless_inbouns.append(vless_inbound)
        new_data["vless"]=vless_inbouns
        await state.finish()
        await new_template.WaitingForVmess.set()
        await state.update_data(data=new_data)

        await update_inbound_keyboard(message_id=callback_query.message.message_id,chat_id=chat_id,protocol='Vmess', state=state)
        
    @dp.callback_query_handler(lambda c: c.data.startswith('Selectvmess_'), state=new_template.WaitingForVmess)
    async def process_select_vmess(callback_query: types.CallbackQuery, state: FSMContext):
        chat_id = callback_query.message.chat.id

        inbound_name = callback_query.data[len('Selectvmess_'):]
        print(inbound_name)  
        # Toggle the selection state in the FSMContext
        current_data = await state.get_data()
        is_selected = current_data.get(inbound_name, False)
        await state.update_data({inbound_name: not is_selected})

        # Update the inline keyboard by editing the message
        print('select vm')
        await update_inbound_keyboard(callback_query.message.message_id,chat_id,'Vmess', state)



    @dp.callback_query_handler(lambda c: c.data.startswith('Selectvless_'), state=new_template.WaitingForVless)
    async def process_select_vless(callback_query: types.CallbackQuery, state: FSMContext):
        chat_id = callback_query.message.chat.id

        inbound_name = callback_query.data[len('Selectvless_'):]
        print(inbound_name)  
        # Toggle the selection state in the FSMContext
        current_data = await state.get_data()
        is_selected = current_data.get(inbound_name, False)
        await state.update_data({inbound_name: not is_selected})

        # Update the inline keyboard by editing the message
        print('select vl')
        await update_inbound_keyboard(callback_query.message.message_id,chat_id,'Vless', state)




