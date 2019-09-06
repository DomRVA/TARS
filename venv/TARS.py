from gtts import gTTS
import speech_recognition as sr
from pygame import mixer

def talk(audio):
    print(audio)
    for line in audio.splitlines():
        text_to_speech = gTTS(text=audio, lang='en')
        text_to_speech.save('audio.mp3')
        mixer.init()
        mixer.music.load('audio.mp3')
        mixer.music.play()
