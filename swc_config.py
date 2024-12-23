import json

class SwConfig:

    def __init__(self, config_file):
        config = self.load_json_config(config_file)
        self.base_url_https = "https://" + config['webserver-address'] + ":" + config['update-port-https']
        self.device = config['rec-device']
        self.threshold = config['noise-threshold']
        self.debug = config['enable-debug']
        self.name = config['device-name']
        self.client_cert = config['client-cert']
        self.client_private_key = config['client-key']

    def load_json_config(self, file_path):
        with open(file_path, 'r') as config_file:
            config = json.load(config_file)
        return config