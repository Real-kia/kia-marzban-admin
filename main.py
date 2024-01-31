from aiogram.dispatcher.filters import Text
from aiogram import executor
import json
import os






file_path = os.path.join(os.path.dirname(__file__), 'config.json')

with open(file_path, 'r') as json_file:
    config_dict = json.load(json_file)

panel_address = config_dict['panel_address']
admin_chat_id= config_dict['admin_chat_id']
panel_username= config_dict['panel_username']
panel_pass = config_dict['panel_pass']


from config import dp, bot


#main menu and start
from handlers.start import start_setup
start_setup()

#dokme haye laqv
from handlers.cancel import cancel_setup
cancel_setup()


#tanzimat tepmlate

from handlers.template import template_add_setup, template_remove_setup, template_setup
template_setup()
template_remove_setup()
template_add_setup()



#tanzimat node
from handlers.node import node_setup, new_node_setup, update_node_setup
node_setup()
new_node_setup()
update_node_setup()

#tanzimat sakhte config
from handlers.cnofig_manage import config_setup, config_create_manual_setup, config_create_template_setup
config_setup()
config_create_manual_setup()
config_create_template_setup()





if __name__ == "__main__":
    executor.start_polling(dp)
