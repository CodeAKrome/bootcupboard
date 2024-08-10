import sys
import time

class SpeechRecognizer:
    def __init__(self, wake_word="jarvis"):
        self.speech_mode = False
        self.imported = False
        self.wake_word = wake_word
        self.stt = None

    def speak(self, val=None) -> bool:
        if val is None:
            return self.speech_mode
        self.speech_mode = val
        return self.speech_mode

    def import_library(self) -> bool:
        if self.imported:
            return True
        try:
            from realtimestt import RealtimeSTT

            self.stt = RealtimeSTT()
            self.imported = True
            return True
        except ImportError:
            print("Please install the RealtimeSTT library by executing the following command:")
            print("pip install realtimestt")
            return False

    def listen(self) -> str:
        if not self.stt:
            print("Speech recognition not initialized. Please call import_library() first.")
            return ""

        print("\rListening...", end='', flush=True)
        
        try:
            text = self.stt.listen()
            if text:
                # Remove the wake word if it's at the beginning of the text
                if text.lower().startswith(self.wake_word.lower()):
                    text = text[len(self.wake_word):].strip()
                print(f"\rYou said: {text}" + " " * 30)
                return text
            else:
                print("\rCould not understand audio." + " " * 30 + "\r", end='', flush=True)
                time.sleep(2)
                print("\r" + " " * 30 + "\r", end='', flush=True)  # Clear the line
                return ""
        except Exception as e:
            print(f"\rError during speech recognition: {e}")
            return ""

recognizer = SpeechRecognizer()

# The rest of the code (cli_input function and main block) remains the same
