import json


def parse_config(path='./settings.json'):
    with open(path, 'r') as f:
        return json.load(f)
