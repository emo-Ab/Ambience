
import requests
import time
import datetime


text_noise = "Sustained Noise levels detected at "
text_quiet = "Things are quiet at "

class NoiseUpdater:
    def __init__(self, baseurl):
        self.base_url = baseurl
        self.servertext = "Noise being detected"

    # Function to update the variable on the Node.js server
    def update_variable(self, value):
        url = f'{self.base_url}?value={value}'
        response = requests.get(url)


    def calculate_latestnoise(self, noise, quiet):
        ts = time.time()
        timeval = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        if (noise > quiet) and (self.servertext != text_noise):
            self.servertext = text_noise
            sendtext = self.servertext + timeval
            self.update_variable(sendtext)
        elif (quiet > noise) and (self.servertext != text_quiet):
            self.servertext = text_quiet
            sendtext = self.servertext + timeval
            self.update_variable(sendtext)
        else:
            time.sleep(1)

