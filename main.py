from swc_config import SwConfig
# from raspi.led_display import LedDisplay
from audio_record.audio_recorder import AudioRecorder
from noise_detection.noise_detector import NoiseDetector
from web_client.web_client import WebClientHttps
import time

if __name__ == '__main__':
    try:
        # load configuration
        swc = SwConfig('config.json')
        noise_detector = NoiseDetector(thres_dB=swc.threshold)
        web_client_node = WebClientHttps(swc.base_url_https, swc.name, swc.client_cert, swc.client_private_key)

        #if swc.device == "RESPEAKER":
        #    led_node = LedDisplay()

        recorder = AudioRecorder(swc.device)
        recorder.start_recording()
        recorder.initPlot()

        while True:
            # Record audio frame
            recorder.record_frame()
            # Calculate spectrogram for latest frame 
            recorder.calculate_spectrogram()
            # recognize speech 
            speech = recorder.recognize_speech()

            if swc.debug == "true":
                # Plot spectrogram on PC
                recorder.plot_spectrogram()
                print(speech)

            # Get noise level from latest spectrogram
            f, sx = recorder.get_spectrogram()
            noise_level = noise_detector.detect_noise(f, sx)

            # Show noise level in LED Display
            # led_node.fader(noise_level)

            # Show noise level in web client
            web_client_node.fader(noise_level, speech)
            time.sleep(0.5)


    except KeyboardInterrupt:
        recorder.clear_cache()
        recorder.stop_recording()
        # if swc.device == "RESPEAKER":
        #    led_node.shutdown()
