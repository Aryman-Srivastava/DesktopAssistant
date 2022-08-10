"""
IMPROVEMENT REQUIRED
"""

import datetime
import json
import os
import pickle
import sys
from youtube_search import YoutubeSearch
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import smtplib
from googlesearch import search

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
url_browser = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"


def search_google(query2):
    links2 = []
    for j in search(term=query2, num_results=5):
        links2.append(j)
    return links2


def cred():
    f = open("login.txt", 'rb')
    content3 = pickle.loads(f.read())
    f.close()
    return content3


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning, Mr. Aryman")
    elif 12 <= hour < 15:
        speak("Good Afternoon, Mr. Aryman")
    else:
        speak("Good Evening, Mr. Aryman")
    speak("I AM FRIDAY, HOW CAN I BE OF HELP TO YOU SIR")
    return None


def takeCommand():
    # IT TAKES MICROPHONE AS INPUT AND PRINTS STATEMENT

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query2 = r.recognize_google(audio, language='en-in')
        print(f'USER SAID: {query2}\n')

    except Exception as e2:
        print(e2)
        speak("SAY THAT AGAIN PLEASE...")
        return None

    return query2


def sendEmail(to2, content2):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    content3 = cred()
    server.login(content3['id'], content3['password'])
    if to2.split()[-1].lower() == "varun":
        server.sendmail(content3['id'], "varun20259@iiitd.ac.in", content2)
    elif to2.split()[-1].lower() == "shiv":
        server.sendmail(content3['id'], "shiv69onb@gmail.com", content2)
    elif to2.split()[-1].lower() == "arjun":
        server.sendmail(content3['id'], "arjun20187@iiitd.ac.in", content2)
    server.close()


if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand()
        if query:
            query = query.lower()
        else:
            continue

        # WIKIPEDIA SEARCH
        if "wikipedia" in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
            except Exception as e:
                query = query.replace(" ", "")
                result = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            # print(result)
            speak(result)

        # OPEN YOUTUBE
        elif "youtube" in query:
            webbrowser.get(url_browser).open("youtube.com")

        # OPEN GOOGLE
        elif "google" in query:
            webbrowser.get(url_browser).open("google.com")

        # OPEN STACKOVERFLOW
        elif "stackoverflow" in query:
            webbrowser.get(url_browser).open("stackoverflow.com")

        # PLAY MUSIC USING YOUTUBE
        elif "play" in query:
            # music_dir = URL HERE
            # songs = os.listdir(music_dir)
            # os.startfile(os.path.join(music_dir, songs[0]))
            speak("opening")
            query = query.replace("play", "")
            results = YoutubeSearch(query, max_results=10).to_json()
            results = json.loads(results)
            url_suffix = results["videos"][0]["url_suffix"]
            url = "https://www.youtube.com/" + url_suffix
            webbrowser.get(url_browser).open(url)

        # TELL TIME
        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        # OPEN PYCHARM
        elif "python" in query:
            pathDir = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2020.2.3\\bin\\pycharm64.exe"
            os.startfile(pathDir)

        # SEND EMAIL
        elif "email" in query:
            try:
                speak("what should i say")
                content = takeCommand()
                speak("to whom should i send the message?")
                to = takeCommand()
                sendEmail(to, content)
                speak("email sent")
            except Exception as e:
                print(e)
                speak("sorry the process has been failed")

        # SEARCH GOOGLE
        elif 'search' in query:
            if query == "search":
                continue
            query = query.replace("search", "")
            links = search_google(query)
            webbrowser.get(url_browser).open(str(links[0]))

        # EXIT
        elif "exit" in query:
            speak("have a great day sir")
            sys.exit()
