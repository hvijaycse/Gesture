from json import loads
import os

def get_config():

    config_filename = "config.json"

    if not  os.path.isfile(f'./{config_filename}'):
        print("Config file does not exist.")

        return None
    else:
        file = open(config_filename, 'r')
        try:
            config = loads(file.read())
            return config
        except:
            return None