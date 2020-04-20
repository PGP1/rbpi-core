import json


def load_config():
    with open('./config/config.json', encoding='utf-8-sig') as configuration:
        config_json = json.load(configuration)

    return config_json
