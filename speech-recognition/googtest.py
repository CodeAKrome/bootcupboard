import speech_recognition as sr

class SpeechToTextListener:
    def __init__(self, wake_word):
        self.wake_word = wake_word
        self.recognizer = sr.Recognizer()
    
    def listen(self):
        with sr.Microphone() as source:
            print("Listening for the wake word...")
            audio = self.recognizer.listen(source)
            
            try:
                transcription = self.recognizer.recognize_google(audio).lower()
                if self.wake_word in transcription:
                    return "Wake word detected. Listening for further commands."
                else:
                    return "Wake word not detected."
            except sr.UnknownValueError:
                return "Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                return f"Could not request results from Google Speech Recognition service; {e}"

def main():
    wake_word = "hey computer"  # Set your wake word here
    listener = SpeechToTextListener(wake_word)
    
    while True:
        response = listener.listen()
        print(response)
        if "wake word detected" in response.lower():
            print("Please say a command:")
            with sr.Microphone() as source:
                audio = listener.recognizer.listen(source)
                try:
                    transcription = listener.recognizer.recognize_google(audio).lower()
                    if "exit" in transcription or "stop" in transcription:
                        print("Exiting...")
                        break
                    else:
                        print(f"You said: {transcription}")
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    main()