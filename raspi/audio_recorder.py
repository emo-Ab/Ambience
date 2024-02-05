import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


class MicConfig:
    def __init__(self, device_name="PC"):        
        if device_name == "PC":
            self.rate=16000
            self.channels=1
            self.device_index=1
            self.frames_per_buffer=1024
        elif device_name == "RESPEAKER":
            self.rate=44100
            self.channels=4
            self.device_index=5
            self.frames_per_buffer=1024

class AudioRecorder:
    def __init__(self, device_name="PC", rec_duration=0.5):
        device = MicConfig(device_name)
        self.channels = device.channels
        self.rate = device.rate
        self.duration = rec_duration
        self.frames_per_buffer = device.frames_per_buffer
        self.device_index = device.device_index        
        self._pa = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.freq = []
        self.times = []
        self.Sxx = []

    def initPlot(self):
        
        # Create a figure and axis
        self.fig, self.ax = plt.subplots()
    
    def start_recording(self):
        self.stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.frames_per_buffer,
                                     input_device_index=self.device_index)

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self._pa.terminate()

    def record_frame(self):
        for index in range(0, int(self.rate / (self.frames_per_buffer * self.duration))):
            audio_sample = np.frombuffer(self.stream.read(self.frames_per_buffer, exception_on_overflow = False),dtype=np.int16)[1::self.channels]
            self.frames.extend(audio_sample.flatten().tolist())        

    def get_spectrogram(self):
        f, sx = self.freq, self.Sxx
        self.clear_cache()
        return f, sx

    def calculate_spectrogram(self):
        #spectrum generation
        self.freq, self.times, self.Sxx = signal.stft(self.frames, fs=self.rate, nperseg=self.frames_per_buffer)
        self.Sxx = np.abs(self.Sxx)
        return 

    def plot_spectrogram(self):
        #plot spectrum 
        plt.pcolormesh(self.times, self.freq, np.abs(self.Sxx))
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        self.fig.canvas.draw()
        plt.pause(0.2)  # pause a bit so that the plot updates
        return

    def clear_cache(self):
        self.frames = []
        self.freq = []
        self.times = []
        self.Sxx = []        