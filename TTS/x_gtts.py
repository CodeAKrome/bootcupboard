from gtts import gTTS

def say(text:str, file:str):
    tts = gTTS(text)
    tts.save(file)


say("Hello, this is a test of gTTS.", "speech.mp3")

#tts = gTTS("Hello, this is a test of gTTS.")
#tts.save("speech.mp3")
