import json
import os
import requests


current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

config_path = os.path.join(parent_dir, 'config.json')

with open(config_path, 'r') as json_file:
    config_dict = json.load(json_file)

panel_address = config_dict['panel_address']

def login(username, password):
    login_url = f"{panel_address}api/admin/token"


    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url=login_url, data=data)
    token = json.loads(response.content)['access_token']

    return token
