import speech_recognition as sr
import time

class SpeechRecognizer:
    def __init__(self, wake_word="jarvis"):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        self.wake_word = wake_word

    def listen_for_wake_word(self):
        """Listens for the wake word and returns True if detected."""
        with self.mic as source:
            print("Listening for wake word...")
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)

        try:
            text = self.r.recognize_google(audio)
            print(f"Heard: {text}")
            return text.lower() == self.wake_word
        except sr.UnknownValueError:
            print("Could not understand audio")
            return False
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return False

    def transcribe_speech(self):
        """Transcribes speech after the wake word is detected."""
        with self.mic as source:
            print("Speak now...")
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)

        try:
            text = self.r.recognize_google(audio)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    while True:
        if recognizer.listen_for_wake_word():
            recognizer.transcribe_speech()
        time.sleep(0.5)
