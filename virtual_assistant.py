from os import error
import os
from os.path import isdir
import pyaudio as audio
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser
import wikipedia
from urllib.request import urlopen
import re
import smtplib
import pathlib
import numpy as np

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speak(msg):
    engine.say(msg)
    engine.runAndWait()

def wish_me():
    current_hour = int(datetime.now().hour)
    if 8<=current_hour<=12:
        speak('Good Morning')
    elif 13<=current_hour<=16:
        speak('Good Afternoon')
    else:
        speak('Good Evening')
    # speak('How may I help you today?')

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        print('Listening...')
        # r.pause_threshold = 1
        r.adjust_for_ambient_noise(mic)
        r.energy_threshold = 100
        command = r.listen(mic)
    try:
        print('Recognizing...')
        query = r.recognize_google(command, language='en-IN')
        print(f'I think you said: {query}\n')
        return query
    except:
        # print(e)
        speak('Say that again, please.')
        return None

def send_email(to, content):
    k = []
    with open('credentials.txt') as f:
        k = f.readlines()
    print(k[0].strip())
    print(k[1].strip())
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(k[0].strip(),k[1].strip())
    result = server.sendmail(k[0], to, content)
    server.close()
    if result != {}:
        speak('There was some error in sending mail')
    else:
        speak(f'Mail sent successfully to {to}')

def do_something():
    speak('How may I help you today?')
    res = None
    while res == None:
        res = take_command()
    res = res.lower()
    print(res)

    try:
        if 'about' in res:
            search_tag = res.split('about')[1].lstrip()
            search_summary = wikipedia.summary(search_tag, sentences=2)
            speak('According to Wikipedia, ')
            # print(search_summary)
            speak(search_summary)

        elif 'open' in res:
            open_tag = res.split('open')[1].lstrip()
            webbrowser.open(url=f'www.{open_tag}.com')
            
        elif 'play' in res:
            play_tag = res.split('play')[1].lstrip()
            play_tag = play_tag.replace(" ", "+")
            youtube_search_URL = 'https://www.youtube.com/results?search_query=' + play_tag
            print(youtube_search_URL)
            html = urlopen(youtube_search_URL)
            video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
            video_song_url = 'https://www.youtube.com/watch?v='+ video_ids[0]
            webbrowser.open(video_song_url)

        elif 'search' in res:
            search_tag = res.split('search')[1].lstrip()
            google_search_URL = 'https://www.google.com/search?q=' + res
            speak('Here is what I found on google.')
            webbrowser.open(google_search_URL)

        elif 'send email' in res:
            speak('Whom do you want to send email?')
            to = take_command()
            speak('Looks good, What should be the content?')
            content = take_command()
            send_email(to.lower().replace(" ", ""), content)
        
        elif 'exit' in res:
            return

        elif 'time' in res:
            speak(datetime.now().strftime('%I%M%p'))

        elif 'pictures' in res:
            # picture_dir = 'C:\\Users\\Shubham\\Pictures'
            picture_dir = os.path.join(pathlib.Path.home(), 'Saved Pictures')
            list_of_pics = os.listdir(picture_dir)
            # [os.startfile(os.path.join(picture_dir, k)) for k in list_of_pics if not os.path.isdir(os.path.join(picture_dir, k))]
            os.startfile(os.path.join(picture_dir, list_of_pics[np.random.randint(0,len(list_of_pics)-1)]))

        else:
            speak("Did you say that correctly? Let's try again.")
            do_something()
    except error as e:
        print(e)
        speak('Something does not look good. Try again later')

if __name__=='__main__':
    speak("What's your name?")
    name = None
    while name==None:
        name = take_command()
    speak(f'Hi! {name}')
    wish_me()

    do_something()
    