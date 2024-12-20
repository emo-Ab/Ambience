import requests
"""
 Generic HTTPS WebClient for updating data to the Web Server
 Configure the end device using config.json
  - https server 
  - a device name
  - Client certificate and key path
  - Device data to update
"""
class WebClientHttps:
    def __init__(self, baseurl_https, dev_name, client_cert, client_key):
        self.base_url_https = baseurl_https
        self.fade_level = 0
        self.device_name = dev_name
        self.cert_path = client_cert
        self.key_path  = client_key

    def update_device_data(self, **kwargs):
        # Ensure the device name is always included
        params = {"device": self.device_name}

        for key, value in kwargs.items():
            print(f"{key}: {value}")

        # Add any additional keyword arguments to the params dictionary
        params.update(kwargs)        

        url = self.base_url_https
        # Currently the TLS handshake does not verify the server certificates
        # InsecureRequestWarning: Unverified HTTPS request is being made to host is seen on console
        # Shall be fixed in future pull requests
        response = requests.get(url, params=params, cert=(self.cert_path, self.key_path), verify=False)
        return response
    

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

	    # Request device data update to the web server
        rgb_value = f"{red_level}, {green_level}, 0"
        response = self.update_device_data(rgb=rgb_value, text=speech_text)
