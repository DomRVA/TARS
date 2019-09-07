from gtts import gTTS
import speech_recognition as sr
from pygame import mixer
import random

def talk(audio):
    print(audio)
    for line in audio.splitlines():
        text_to_speech = gTTS(text=audio, lang='en')
        text_to_speech.save('audio.mp3')
        mixer.init()
        mixer.music.load('audio.mp3')
        mixer.music.play()

def myCommand():
    #Initialize the recognizer
    r=sr.Recognizer()

    with sr.Microphone() as source:
        print('TARS is Ready...')
        r.pause_threshold = 1
        #wait for a second to let the reconizer adjust the
        #energy threshold based on the surroudning nois level
        r.adjust_for_ambient_noise(source, duration=1)
        #listens for the usser's input
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\r')

    #loop back to continue to listen for commands if unrocongnizable speec is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand();

    return command

def tars(command):
    errors=[
        "I don\'t know what you mean!",
        "Excuse me?",
        "Can you repeat it please?"
    ]

    if 'Hello' in command:
        talk('Hello! I am TARS.  How can I help you?')

    else:
        error = random.choice(errors)
        talk(error)

talk('TARS is ready!')

#loop to continue executing multiple commands
while True:
    tars(myCommand())