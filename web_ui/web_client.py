import requests

class WebClient:
    def __init__(self, baseurl, dev_name):
        self.base_url = baseurl
        self.fade_level = 0
        self.device_name = dev_name

    # Function to update latest device data on the Node.js server
    def update_device_data(self, rgb_value, text_value):
        url = f'{self.base_url}?device={self.device_name}&rgb={rgb_value}&text={text_value}'
        response = requests.get(url)

    def tune(self):
        #maintain fader levels between 10 - 90
        if self.fade_level>90:
            self.fade_level=90
        elif self.fade_level<=10:
            self.fade_level=10

    def fader_step(self):
        #determine step level for UI fader
        if self.fade_level > 75:
            return 12
        elif self.fade_level > 50:
            return 13
        elif self.fade_level > 25:
            return 14
        else:
            return 15

    def fader(self, noise_level, speech_text):
        #UI fader
        self.tune()

        if noise_level == "noise detected":
            self.fade_level+=self.fader_step()
        elif noise_level == "silence":
            self.fade_level-=self.fader_step()

        red_level = self.fade_level
        green_level = 100 - self.fade_level

	    # Update the noise levels to the web server
        rgb_value = f"{red_level}, {green_level}, 0"
        self.update_device_data(rgb_value, speech_text)
