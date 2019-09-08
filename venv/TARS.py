from gtts import gTTS
import speech_recognition as sr
from pygame import mixer
import random
import re
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
import bs4
import requests

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

if 'open google and search' in command:
    #matching command to chack it is available
    reg_ex = re.search('open google and search (.*)', command)
    search_for = command.split("search",1)[1]
    url = 'https://www.google.com/'
    if reg_ex:
        subgoogle = reg_ex.group(1)
        url = url + 'r/' + subgoogle
    talk('Okay!')
    driver = webdriver.Firefox
    driver.get('http://www.google.com')
    search = driver.find_element_by_name('q') #finds search
    search.send_keys(str(search_for)) #sends search keys
    search.send_keys(Keys.RETURN) #hits enter
    webbrowser.open(url)
    print('Done!')

elif 'email' or 'gmail' in command:
    talk('What is the subject?')
    time.sleep(3)
    subject = myCommand()
    talk('What should I say?')
    time.sleep(3)
    message = myCommand()
    content = 'Subject: {}\n\n{}'.format(subject,message)

    #init gmail SMTP
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    #identifytoserver
    mail.ehlo()

    #encrypt session
    mail.starttls()

    #login
    mail.login('your_gmail', 'your_password')  ####SOOOOOO Insecure.  NO! find a better way

    #send message
    mail.sendmail('FROM', 'TO', content)

    #end mail connection
    mail.close()

    talk('Email sent.')

elif 'wikipedia' in command:
    reg_ex = re.search('search in wikipedia (.+)', command)
    if reg_ex:
        query = command.split()
        response = requests.get("https://en.wikpedia.org/wiki/" + query[3])

        if response is not None:
            html = bs4.BeautifulSoup(response.text, 'html.parser')
            title = html.select("#firstHeading")[0].text
            paragraphs = html.select("p")
            for para in paragraphs:
                print(para.text)

#loop to continue executing multiple commands
while True:
    tars(myCommand())