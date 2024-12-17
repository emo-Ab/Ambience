import requests

class WebClient:
    def __init__(self, baseurl, dev_name):
        self.base_url = baseurl
        self.fade_level = 0
        self.update_device_name(dev_name)

    # Function to update the rgb value on the Node.js server
    def update_device_name(self, value):
        url = f'{self.base_url}?device={value}'
        response = requests.get(url)
        
    # Function to update the rgb value on the Node.js server
    def update_variable(self, value):
        url = f'{self.base_url}?value={value}'
        response = requests.get(url)

    # Function to update the recognized speech on the Node.js server
    def update_speech(self, text):
        url = f'{self.base_url}?text={text}'
        response = requests.get(url)

    def send_noise_level(self, red, green):
        send_text = f"{red}, {green}, 0"
        self.update_variable(send_text)


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

    def fader(self, val):
        #UI fader
        self.tune()

        if val == "noise detected":
            self.fade_level+=self.fader_step()
        elif val == "silence":
            self.fade_level-=self.fader_step()

        red_level = self.fade_level
        green_level = 100 - self.fade_level

	    # Update the noise levels to the web server
        self.send_noise_level(red_level, green_level)

    def speech_to_text(self, text):
        # Send recognized speech to web server
        self.update_speech(text)
        return