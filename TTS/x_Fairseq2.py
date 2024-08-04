from TTS.api import TTS

dataset = 'universal',


#api = TTS(model_name="tts_models/eng/fairseq/vits").to("cuda")
#api = TTS(model_name="tts_models/eng/fairseq/vits").to("mps")
api = TTS(model_name="tts_models/eng/universal/fairseq/vits").to("mps")

api.tts_to_file("This is a test.", file_path="output.wav")

# TTS with on the fly voice conversion
api = TTS("tts_models/deu/fairseq/vits")
api.tts_with_vc_to_file(
    "Wie sage ich auf Italienisch, dass ich dich liebe?",
    speaker_wav="gandalf.wav",
    file_path="ouptut.wav"
)