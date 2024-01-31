from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


startkeyboard = InlineKeyboardMarkup()
config_manage_keyboard = InlineKeyboardButton('مدیریت کانفیگ', callback_data='manage_config')
node_manage_btn = InlineKeyboardButton('تنظیمات نود', callback_data = 'node_setting')
startkeyboard.add(config_manage_keyboard).add(node_manage_btn)

cancel_menu = InlineKeyboardMarkup()
cancel_btn_inline =InlineKeyboardButton("لغو", callback_data='cancelask')
cancel_menu.add(cancel_btn_inline)

main_menu_btn = InlineKeyboardButton('بازگشت به منو اصلی', callback_data='main_menu')

node_menu = InlineKeyboardMarkup()
add_node_btn = InlineKeyboardButton('افزودن نود', callback_data='add_node')
update_node_btn = InlineKeyboardButton('آپدیت نود', callback_data='update_node')
node_menu.add(add_node_btn).add(update_node_btn).add(main_menu_btn)



config_keyboard = InlineKeyboardMarkup()
manage_template_btn = InlineKeyboardButton('مدیریت تمپلیت ها', callback_data='manage_template')
config_create_btn = InlineKeyboardButton('ساخت کانفیگ', callback_data = 'config_create')
config_keyboard.add(manage_template_btn).add(config_create_btn).add(main_menu_btn)

