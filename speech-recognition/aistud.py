import speech_recognition as sr
import time

# Initialize recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Set wake word
WAKE_WORD = "jarvis"

def listen_for_wake_word():
    """Listens for the wake word and returns True if detected."""
    with mic as source:
        print("Listening for wake word...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"Heard: {text}")
        return text.lower() == WAKE_WORD
    except sr.UnknownValueError:
        print("Could not understand audio")
        return False
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return False

def transcribe_speech():
    """Transcribes speech after the wake word is detected."""
    with mic as source:
        print("Speak now...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    while True:
        if listen_for_wake_word():
            transcribe_speech()
        time.sleep(0.5)  # Small delay to prevent excessive CPU usage
