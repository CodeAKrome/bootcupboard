#!/usr/bin/env python3
import sys

from kittentts import KittenTTS
m = KittenTTS("KittenML/kitten-tts-nano-0.1")

txt = sys.stdin.read().strip()

audio = m.generate(txt, voice='expr-voice-2-f' )

# available_voices : [  'expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f',  'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f' ]

# Save the audio
import soundfile as sf
sf.write('output.wav', audio, 24000)
