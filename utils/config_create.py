import requests
import os
import json
import re
import uuid
import random

from utils.login import login

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

config_path = os.path.join(parent_dir, 'config.json')

with open(config_path, 'r') as json_file:
    config_dict = json.load(json_file)

panel_address = config_dict['panel_address']
panel_username = config_dict['panel_username']
panel_pass = config_dict['panel_pass']




def generate_numbers(value, i):
    if value[-1].isdigit():
        last_number = ''
        for char in reversed(value):
            if char.isdigit():
                last_number = char + last_number
            else:
                break
        start_number = int(last_number) + 1
        end_number = start_number + i
        return list(range(start_number, end_number))
    else:
        return list(range(1, i + 1))
   


def bulk_config_create(name,hajm, days, tedad, inbounds, token):
    hajm = int(hajm)
    days = int(days)
    tedad = int(tedad)
    sub_links = []
    new_usernames = []
    if tedad > 1:
        username_main = name

        numbers = generate_numbers(username_main, tedad)
        for number in numbers:
            if any(char.isdigit() for char in username_main):
                username_main =re.sub(r'\d+$', '', username_main)
                new_usernames.append(username_main+str(number))
            else:
                new_usernames.append(username_main+str(number))
    else:
        new_usernames.append(name)



    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    for new_username in new_usernames:
        response = requests.get(f'{panel_address}api/users', headers=headers)
        users = json.loads(response.content)['users']
        usernames = []

        uuidd = str(uuid.uuid4())
        found = False
        for user in users:
            username = user['username']
            usernames.append(username)
            sub_link = user['subscription_url']
            if username == new_username:
                found = True
                print(username)
                break
        if found == False: #new user

            json_data = {
                'username': f'{new_username}',
                'note': '',
                'proxies': {},
                'data_limit': 1073741824* int(hajm),
                'expire': None,
                'data_limit_reset_strategy': 'no_reset',
                "status": "on_hold",
                "note": "",

                "on_hold_expire_duration": 86400* int(days),
                'inbounds': inbounds
            }
            if 'vless' in inbounds:
                json_data['proxies']['vless'] = {
                        'id': uuidd,
                        'flow': 'xtls-rprx-vision',
                    }
            if 'vmess' in inbounds:

                json_data['proxies']['vmess'] = {
                        'id': uuidd,
                    }


            response = requests.post(f'{panel_address}api/user', headers=headers, json=json_data)
            print(response.content)
            sub_link = json.loads(response.content)['subscription_url']
            sub_links.append(sub_link)
    return sub_links