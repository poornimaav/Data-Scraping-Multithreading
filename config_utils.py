import json

def read_config(filename):
    with open(filename, 'r') as config_file:
        config_data = json.load(config_file)
    return config_data


config_filename = "config.json"
config = read_config(config_filename)

def write_config(config):
    with open(config_filename, "w") as config_file:
        json.dump(config, config_file, indent=4)