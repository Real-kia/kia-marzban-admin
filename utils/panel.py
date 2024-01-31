import requests
import os
import json


from utils.login import login

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)

config_path = os.path.join(parent_dir, 'config.json')

with open(config_path, 'r') as json_file:
    config_dict = json.load(json_file)

panel_address = config_dict['panel_address']
panel_username = config_dict['panel_username']
panel_pass = config_dict['panel_pass']


def get_templates():
    token = login(panel_username, panel_pass)
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(f'{panel_address}api/user_template', headers=headers)
    template_list = json.loads(response.text)
    return template_list


def get_inbounds():
    token = login(panel_username, panel_pass)
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(f'{panel_address}api/inbounds', headers=headers)
    return json.loads(response.text)


def get_node_id(node_name):
    token = login(panel_username, panel_pass)
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
    } 
    response = requests.get(f'{panel_address}api/nodes', headers=headers)
    nodes_list = json.loads(response.text)
    found = False

    for node in nodes_list:
        if node['name'] == node_name:
            found = True
            return node['id']

    if found == False:
        return "Not Found"


def get_node_default(node_id, var):
    token = login(panel_username, panel_pass)
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
    } 
    response = requests.get(f'{panel_address}api/node/{node_id}', headers=headers)
    node_detail = json.loads(response.text)
    return node_detail[var]
