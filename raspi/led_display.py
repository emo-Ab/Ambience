import apa102
import time
import threading
from scipy import signal
from gpiozero import LED
import pyaudio
import wave
import numpy as np
import audioop
from update_noise_detected import NoiseUpdater

class LedDisplay:
    PIXELS_N = 12

    def __init__(self):
        self.dev = apa102.APA102(num_led=self.PIXELS_N)
        self.power = LED(5)
        self.power.on()
        self.fill_level = 0
        self.updater = NoiseUpdater('http://192.168.0.31:8080/')


    def show(self, data):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]))
        self.dev.show()


    def calibrate(self):
        #maintain fader levels between 10 - 90
        if self.fill_level>90:
            self.fill_level=90
        elif self.fill_level<=10:
            self.fill_level=10

    def fadevalue(self):
        #determine rise/lower level for led brightness
        if self.fill_level > 75:
            return 2
        elif self.fill_level > 50:
            return 3
        elif self.fill_level > 25:
            return 4
        else:
            return 5

    def fader(self, val):

        self.calibrate()

        if val == "noise detected":
            self.fill_level+=self.fadevalue()
        elif val == "silence":
            self.fill_level-=self.fadevalue()

        red_led = self.fill_level
        green_led = 100 - self.fill_level


	    # Update the noise levels to the web server
        self.updater.calculate_latestnoise(red_led, green_led)

        #print(val)
        #print(red_led)

        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, red_led,green_led, 0, 50)
        self.dev.show()
