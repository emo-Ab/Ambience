import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


class NoiseDetector:
    def __init__(self, thres_freq=20, thres_ampl=145, thres_dB=15):
        self.threshold_freq=thres_freq
        self.threshold_ampl=thres_ampl
        self.threshold_dB = thres_dB
        self.noise_history = []

    def calculate_noiselevel(self, frame):
        rms = np.sqrt(np.mean(frame))
        noise_level= 20 * np.log10(rms)
        return noise_level
    
    def get_noise_history(self):
        return self.noise_history
    
    def detect_noise(self, freq, frame):
        noise_level = self.calculate_noiselevel(frame)
        #print(noise_level)
        if noise_level>self.threshold_dB:
            count_noise="noise detected"
            self.noise_history.append(1)
        else:
            count_noise="silence"
            self.noise_history.append(0)
        return count_noise
    
    def calc_noise_history(self):
        slope = np.polyfit(range(len(self.noise_history)), self.noise_history, 1)[0]
        return slope