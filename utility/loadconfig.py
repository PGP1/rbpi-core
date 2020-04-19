import json


def load_config():
    with open('./config/config.json', encoding='utf-8-sig') as configuration:
        config_file = configuration.read()
        config_json = json.load(config_file)

    return config_json
