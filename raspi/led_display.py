import apa102
import time
import threading
from scipy import signal
from gpiozero import LED
try:
    import queue as Queue
except ImportError:
    import Queue as Queue
import pyaudio
import wave
import numpy as np
import audioop
from alexa_led_pattern import AlexaLedPattern
from update_noise_detected import NoiseUpdater

class LedDisplay:
    PIXELS_N = 12

    def __init__(self, pattern=AlexaLedPattern):
        self.pattern = pattern(show=self.show)
        self.dev = apa102.APA102(num_led=self.PIXELS_N)
        self.power = LED(5)
        self.power.on()
        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        self.last_direction = None
        self.fill_level = 0
        self.updater = NoiseUpdater('http://localhost:8080')

    def show(self, data):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]))
        self.dev.show()

    def off(self):
        self.put(self.pattern.off)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)


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
