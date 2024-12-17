import json

class SwConfig:

    def __init__(self, config_file):
        config = self.load_json_config(config_file)
        self.server_ip = "http://" + config['webserver-address'] + ":" + config['update-port'] + "/"
        self.device = config['rec-device']
        self.threshold = config['noise-threshold']
        self.debug = config['enable-debug']
        self.name = config['device-name']

    def load_json_config(self, file_path):
        with open(file_path, 'r') as config_file:
            config = json.load(config_file)
        return config