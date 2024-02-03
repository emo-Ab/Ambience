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
        self.currentstate = 0

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
        
    def fader(self, val):
        if val == "noise detected":
            self.currentstate+=10
        elif self.currentstate>10:
            self.currentstate-=10
        abs_val = self.currentstate%100
        red_led = abs_val
        green_led = 100 - abs_val
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, red_led,green_led, 0, 80)
        self.dev.show()

    def led_lightup(self):
        timer = threading.Timer(1, self.fader("silence"))
        timer.start()

try:
    pixels = LedDisplay()

    while True:
        # Test the function
        for i in range(101):
            pixels.fader(i)

except KeyboardInterrupt:
    # Stop LEDs when Ctrl+C is pressed
    pixels.off()