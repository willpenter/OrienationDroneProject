import speech_recognition as sr
from droneControl import DroneController

def recognizeSpeech(recognizer, microphone):
    with microphone as mp:
        #print("Listeing...")
        recognizer.adjust_for_ambient_noise(mp)
        audioRes = recognizer.listen(mp)

    try:
        #print("Recognizing...")
        return recognizer.recognize_google(audioRes)
    except sr.RequestError:
        print("API call fail")
    except sr.UnknownValueError:
        print("Couldn't recognize speech")

    return ""

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    controller = DroneController()
    controller.connect()

    try:
        while True:
            recognizedText = recognizeSpeech(recognizer, microphone)
            
            print(f"Result from recognized: {recognizedText}")

            if recognizedText.lower() == "take off":
                controller.takeoff()
            elif recognizedText.lower() == "land":
                controller.land()
            # more voice commands here

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        controller.land()

if __name__ == "__main__":
    main()