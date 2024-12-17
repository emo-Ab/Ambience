from swc_config import SwConfig
from audio.audio_recorder import AudioRecorder
from process.noise_detector import NoiseDetector
from web_ui.web_display import WebDisplay
import time

if __name__ == '__main__':
    try:
        # load configuration
        swc = SwConfig('config.json')
        noise_detector = NoiseDetector(thres_dB=swc.threshold)
        web_client_node = WebDisplay(swc.server_ip)

        recorder = AudioRecorder(swc.device)
        recorder.start_recording()
        recorder.initPlot()

        while True:
            # Record audio frame
            recorder.record_frame()
            # Calculate spectrogram for latest frame 
            recorder.calculate_spectrogram()

            if swc.device == "PC":
                # Plot spectrogram on PC
                recorder.plot_spectrogram()

            # Get noise level from latest spectrogram
            f, sx = recorder.get_spectrogram()
            noise_level = noise_detector.detect_noise(f, sx)

            if swc.device == "RESPEAKER":
                from raspi.led_display import LedDisplay
                led_node = LedDisplay()
                # Show noise level in LED Display
                led_node.fader(noise_level)


            # Show noise level in web client
            web_client_node.fader(noise_level)


            time.sleep(1)


    except KeyboardInterrupt:
        recorder.clear_cache()
        recorder.stop_recording()
        if swc.device == "RESPEAKER":
            led_node.shutdown()

