"""
THIS IS A DESKTOP ASSISTANT CALLED FRIDAY.

**IT IS REQUESTED BY THE USER TO UPDATE THEIR EMAIL LOGIN DETAILS FIRST BY CREATING A TEXT FILE
login.txt AND CREATING A LIST OF PEOPLE TO WHOM THEY WANT TO MAIL

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
# TYPE THE PATH OF CHROME OR ANY OTHER PREFERRED BROWSER HERE
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

    # UPDATE THE LIST OF USERNAME THAT USER WANTS TO SEND EMAILS TO
    # if to2.split()[-1].lower() == "NAME THAT USER WANTS TO SEND THE MESSAGE TO EXAMPLE FOR VARUN TYPE VARUN":
    #     server.sendmail(content3['id'], "EMAIL WANT TO SEND THE MAIL TO", content2)

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
            try:
                webbrowser.get(url_browser).open("youtube.com")
            except Exception as e:
                webbrowser.open("youtube.com")

        # OPEN GOOGLE
        elif "google" in query:
            try:
                webbrowser.get(url_browser).open("google.com")
            except Exception as e:
                webbrowser.open("google.com")

        # OPEN STACKOVERFLOW
        elif "stackoverflow" in query:
            try:
                webbrowser.get(url_browser).open("stackoverflow.com")
            except Exception as e:
                webbrowser.open("stackoverflow.com")

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
            try:
                webbrowser.get(url_browser).open(url)
            except Exception as e:
                webbrowser.open(url)

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
            try:
                webbrowser.get(url_browser).open(str(links[0]))
            except Exception as e:
                webbrowser.open(str(links[0]))

        # FINDING FILE IN OS
        elif 'os' in query.lower():
            query = query.replace("os ", "")
            query = query.replace("OS ", "")
            query = query.replace("Os ", "")
            query = query.replace("oS ", "")
            result = []
            for root, _, files in os.walk("C:"):
                if query.lower() in files:
                    result.append(os.path.join(root, query))
            if result:
                os.startfile(result[0])
            else:
                speak("file not found")

        # EXIT
        elif "exit" in query:
            speak("have a great day sir")
            sys.exit()
