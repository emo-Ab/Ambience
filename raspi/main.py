from audio_recorder import AudioRecorder
from audio_recorder import MicConfig
from led_display import LedDisplay
from noise_detector import NoiseDetector
import datetime
import time

if __name__ == '__main__':
    try:
        pixels = LedDisplay()
        noiser = NoiseDetector(thres_dB=10)

        # Use PC
        recorder = AudioRecorder("RESPEAKER")
        recorder.start_recording()
        recorder.initPlot()

        while True:
            # Record a frame
            recorder.record_frame()
            # Calculate the spectrogram for the latest frame
            recorder.calculate_spectrogram()
            #Plot spectorgram 
            #recorder.plot_spectrogram()
            f, sx = recorder.get_spectrogram()
            # Test noise detection
            value = noiser.detect_noise(f, sx)
            pixels.fader(value)
            time.sleep(1)


    except KeyboardInterrupt:
        # Stop LEDs when Ctrl+C is pressed
        recorder.clear_cache()
        recorder.stop_recording()
        pixels.off()

