from config import dp, bot
from keyboards.keybaords import node_menu, cancel_menu
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import os
import json
import requests
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils.panel import get_node_id, get_node_default
from utils.login import login


current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

config_path = os.path.join(parent_dir, 'config.json')

with open(config_path, 'r') as json_file:
    config_dict = json.load(json_file)

panel_address = config_dict['panel_address']
panel_username = config_dict['panel_username']
panel_pass = config_dict['panel_pass']

def node_setup():
    @dp.callback_query_handler(text=["node_setting"])
    async def node_setting(callback_query: types.CallbackQuery, state: FSMContext):
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id


        # Edit the message text


        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="گزینه مورد نظر را انتخاب کنید", reply_markup=node_menu)



class node_update(StatesGroup):
    WaitingForNodeName= State()
    WaitingForNodeIp = State()
    WaitingForNodePort = State()
    WaitingForNodeApiPort = State()
    WaitingForZarib = State()


def update_node_setup():
# update node



    @dp.callback_query_handler(text=["update_node"])
    async def ask_node_name(callback_query: types.CallbackQuery, state: FSMContext):
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id


        # Edit the message text
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="اسم را وارد کنید", reply_markup=cancel_menu)

        await node_update.WaitingForNodeName.set()

    @dp.message_handler(state=node_update.WaitingForNodeName)
    async def proces_node_name(message: types.Message, state: FSMContext):


        name = message.text
        id = get_node_id(name)
        if id == "Not Found":
            await state.finish()
            await message.reply('نود یافت نشد !!', reply_markup=node_menu)
        else:
            chat_id = message.chat.id

            await state.update_data(id=id)


            await bot.send_message(text=f'آیپی نود را وارد کنید\nبرای تغییر ندادن ایپی\n/default\nرا بزنید' ,chat_id=chat_id, reply_markup=cancel_menu)

            await node_update.WaitingForNodeIp.set()
    @dp.message_handler(state=node_update.WaitingForNodeIp)
    async def proces_ip(message: types.Message, state: FSMContext):


        ip = message.text
        chat_id = message.chat.id

        await state.update_data(ip=ip)

        
        await bot.send_message(text='(به طور دیفالت 62050)پورت نود را وارد کنید\nبرای تغییر ندادن \n/default\nرا وارد کنید' ,chat_id=chat_id, reply_markup=cancel_menu)

        await node_update.WaitingForNodePort.set()


    @dp.message_handler(state=node_update.WaitingForNodePort)
    async def proces_port(message: types.Message, state: FSMContext):


        port = message.text
        chat_id = message.chat.id

        await state.update_data(port=port)


        await bot.send_message(text='(به طور دیفالت 62051)apiport نود را وارد کنید\nبرای تغییر ندادن \n/default\nرا وارد کنید' ,chat_id=chat_id, reply_markup=cancel_menu)

        await node_update.WaitingForNodeApiPort.set()
    @dp.message_handler(state=node_update.WaitingForNodeApiPort)
    async def proces_apiport(message: types.Message, state: FSMContext):


        apiport = message.text
        chat_id = message.chat.id

        await state.update_data(apiport=apiport)


        await bot.send_message(text='ضریب نود را وارد کنید' ,chat_id=chat_id, reply_markup=cancel_menu)

        await node_update.WaitingForZarib.set()





    @dp.message_handler(state=node_update.WaitingForZarib)
    async def proces_zarib(message: types.Message, state: FSMContext):


        zarib = float(message.text)
        chat_id = message.chat.id


        data = await state.get_data()
        id = data['id']


        ip = data['ip']
        if ip == '/default':
            ip = get_node_default(id, 'address')
        port = data['port']
        if port == '/default':
            port = get_node_default(id, 'port')
        else:
            port = int(port)
        apiport = data['apiport']
        if apiport == '/default':
            apiport = get_node_default(id, "api_port")
        else:
            apiport = int(apiport)

        await state.finish()






        token = login(panel_username, panel_pass)
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}',
        }

        json_data = {
            'address': ip,
            'port': port,
            'api_port': apiport,
            'usage_coefficient': zarib,
        }


        response = requests.put(f'{panel_address}api/node/{id}', headers=headers, json=json_data)
        await message.reply(response.text)



#add and update node


class new_node(StatesGroup):
    WaitingForNodeName= State()
    WaitingForNodeIp = State()
    WaitingForNodePort = State()
    WaitingForNodeApiPort = State()
    WaitingForZarib = State()

def new_node_setup():
    @dp.callback_query_handler(text=["add_node"])
    async def ask_node_name(callback_query: types.CallbackQuery, state: FSMContext):
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id


        # Edit the message text
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="اسم را وارد کنید", reply_markup=cancel_menu)

        await new_node.WaitingForNodeName.set()

    @dp.message_handler(state=new_node.WaitingForNodeName)
    async def proces_node_name(message: types.Message, state: FSMContext):


        name = message.text
        chat_id = message.chat.id

        await state.update_data(name=name)


        await bot.send_message(text='آیپی نود را وارد کنید' ,chat_id=chat_id, reply_markup=cancel_menu)

        await new_node.WaitingForNodeIp.set()
    @dp.message_handler(state=new_node.WaitingForNodeIp)
    async def proces_ip(message: types.Message, state: FSMContext):


        ip = message.text
        chat_id = message.chat.id

        await state.update_data(ip=ip)


        await bot.send_message(text='(به طور دیفالت 62050)پورت نود را وارد کنید' ,chat_id=chat_id, reply_markup=cancel_menu)

        await new_node.WaitingForNodePort.set()


    @dp.message_handler(state=new_node.WaitingForNodePort)
    async def proces_port(message: types.Message, state: FSMContext):


        port = message.text
        chat_id = message.chat.id

        await state.update_data(port=port)


        await bot.send_message(text='(به طور دیفالت 62051)apiport نود را وارد کنید' ,chat_id=chat_id, reply_markup=cancel_menu)

        await new_node.WaitingForNodeApiPort.set()
    @dp.message_handler(state=new_node.WaitingForNodeApiPort)
    async def proces_apiport(message: types.Message, state: FSMContext):


        apiport = message.text
        chat_id = message.chat.id

        await state.update_data(apiport=apiport)


        await bot.send_message(text='ضریب نود را وارد کنید' ,chat_id=chat_id, reply_markup=cancel_menu)

        await new_node.WaitingForZarib.set()





    @dp.message_handler(state=new_node.WaitingForZarib)
    async def proces_zarib(message: types.Message, state: FSMContext):


        zarib = float(message.text)
        chat_id = message.chat.id


        data = await state.get_data()
        name = data['name']
        ip = data['ip']
        port = int(data['port'])
        apiport = int(data['apiport'])

        await state.finish()



        token = login(panel_username, panel_pass)
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}',
        }

        json_data = {
            'name': name,
            'address': ip,
            'port': port,
            'api_port': apiport,
            'add_as_new_host': False,
            'usage_coefficient': zarib,
        }

        response = requests.post(f'{panel_address}api/node', headers=headers, json=json_data)
        await message.reply(response.text)
        response_add = json.loads(response.text)


        await message.reply(f'نود اضافه شد\nدر حال اعمال ضریب')
        token = login(panel_username, panel_pass)
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {token}',
        }

        json_data = {
            'address': ip,
            'port': port,
            'api_port': apiport,
            'usage_coefficient': zarib,
        }
        id = int(response_add['id'])
        response = requests.put(f'{panel_address}api/node/{id}', headers=headers, json=json_data)
        await message.reply(response.text)


