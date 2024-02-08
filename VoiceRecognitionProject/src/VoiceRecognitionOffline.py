import os
import json
import pyaudio
from djitellopy import Tello
from vosk import Model, KaldiRecognizer
from droneControl import DroneController

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    modelPath = os.path.join(script_dir, '..', 'models', 'vosk-model-small-en-us-0.15')

    model = Model(modelPath)
    recognizer = KaldiRecognizer(model, 16000)

    pAud = pyaudio.PyAudio()
    voiceStream = pAud.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    voiceStream.start_stream()

    tello = Tello()
    tello.connect()

    try:
        while True:
            data = voiceStream.read(4096)

            if recognizer.AcceptWaveform(data):
                resultJson = recognizer.Result()
                resultDict = json.loads(resultJson)
                recognizedText = resultDict.get('text', '')

                print(f"Result from recognized: {recognizedText}")

                if recognizedText == "take off":
                    tello.takeoff()
                elif recognizedText == "land":
                    tello.land()
                # more voice commands here

    except KeyboardInterrupt:
        print("\nExiting...")
        
    finally:
        tello.land()
        voiceStream.stop_stream()
        voiceStream.close()
        pAud.terminate()

if __name__ == "__main__":
    main()