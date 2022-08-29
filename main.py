import os
import re
import subprocess
import webbrowser
from datetime import datetime

import speech_recognition as sr
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
#for spotipy go to oauth2.py and change ID and Client Secret

favwebsites = {
    "facebook": "facebook.com",
    "instagram": "instagram.com",
    "google": "google.com",
    "youtube": "youtube.com",
    "amu": "amu.edu.pl",
    "wp": "wp.pl",
    "interia": "interia.pl"
}

speech_rec = False

path = 'C:\\Users\\Kamiko\\Desktop\\'

def getInput():
    if speech_rec:
        while True:
            guess = speech_recognize()
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I don't understand! Try again!")
            if guess["error"]:
                print("ERROR: {}".format(guess["error"]))
                break
        command = str(guess["transcription"]).lower()
        print("You said: {}".format(guess["transcription"]))
    else:
        command = input()
    return command


def speech_recognize():
    r = sr.Recognizer()
    mic = sr.Microphone()

    if not isinstance(r, sr.Recognizer):
        raise TypeError('r must be Recognizer instance')

    if not isinstance(mic, sr.Microphone):
        raise TypeError('mic must be Microphone instance')

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = r.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response


def opensth(string):
    print("Opening:", string)
    app = True
    site = True
    try:
        openProgram(string)
    except:
        app = False
    if not app:
        try:
            openFile(string)
        except:
            site = False
    if not site:
        openWebsite(string)


def openFile(filename):
        os.startfile(path+filename)


def openProgram(name):
    os.startfile(name+".exe")


def run(string):
    try:
        openProgram(string)
    except:
        print("App", string, "not found")


def show(string):
    try:
        openFile(string)
    except:
        print("File", string, "not found")


def makeNote():
    print("What do you want me to write down?")
    note = getInput()
    date = datetime.now()
    name = str(date).replace(":", "-") + "-note.txt"
    with open(name, "w") as f:
        f.write(note)

    subprocess.Popen(["notepad.exe", name])


def closeProgram(name):
    try:
        print("Closing:", name)
        os.system("TASKKILL /F /IM "+name+".exe")
    except:
        print("Sorry, I don't know this program")


def openWebsite(url):
    if re.match('https://.+\.[a-z]{,3}', url):
        webbrowser.open(url)
    elif re.match(".+\.[a-z]{,3}", url):
        webbrowser.open('https://'+url)

    #to make speech recognition easier
    elif url in favwebsites:
        site = favwebsites[url]
        print('redirecting:', site)
        webbrowser.open_new_tab("https://"+site)

    else:
        query= "https://www.google.com.tr/search?q={}".format(url)
        webbrowser.open_new_tab(query)


def google(query):
    url = "https://www.google.com.tr/search?q={}".format(query)
    print("Searching for: ", query)
    webbrowser.open_new_tab(url)


def spotify_player():
    found = False
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())


    print("Which song you want me to play? (title)")
    song_title = getInput()

    print("Artist:")
    name_artist = getInput()

    searchResult = spotify.search(q='artist:' + name_artist, type='artist')
    items = searchResult['artists']['items']
    if len(items) > 0:
        artist = items[0]
        uri = artist['uri']
        print(artist['name'], "-", song_title)


    searchTrack = spotify.search(q='track:' + song_title, type='track')

    items = searchTrack['tracks']['items']
    for track in items:
        name = track['artists'][0]['name']
        if name.lower() == artist['name'].lower():
            print(track['name'], ":", track['external_urls'])
            found = True

    if not found:
        print("Sorry, i couldn't find it")


def addWebsite():
    print("Paste short url here: (ex. google.com)")
    url = input()
    print("How do you want to call it?")
    name = getInput()

    favwebsites[name] = url

    print("Saved websites: ", favwebsites)


def help():
    print("Hello! \n There are commands you can use:")
    print("1. Speech - turn on speech recognition")
    print("2. Run (app) - open app you want")
    print("3. Open (app/file/website url) - open app, file or website you want")
    print("4. Show (filename) - open file")
    print("5. Spotify - turn on spotify API on this console \n (Spotify api let's you search "
          "for your favourite music inside console)")
    print("6. Note - open notepad with a note you want (makes sense with speech recognition on)")
    print("7. Google (phrase) - google stuff for you")
    print("8. Add website - let's you add website to list (helpful with speech recognition)")


def get_name(string):
    command = string.split(" ")
    name = ' '.join(command[1:])
    return name

def check_command(string):
    global speech_rec

    #TODO: change handling given commands

    if string == "help":
        help()

    if re.search(r".*speech.*", string):
        print("Speech recognition: ON \n Say 'STOP' to disable speech recognition")
        speech_rec = True
    elif string == "stop" and speech_rec:
        speech_rec = False
        print("Speech recognition: OFF")
    elif re.search(r".*spotify", string):
        spotify_player()
    elif re.search(r"run .+", string):
        name = get_name(string)
        run(name)
    elif re.search(r"close .+", string):
        name = get_name(string)
        closeProgram(name)
    elif re.search(r"open .+", string):
        name = get_name(string)
        opensth(name)
    elif re.search(r"show .*", string):
        name = get_name(string)
        show(name)
    elif re.search(r"google .*", string):
        name = get_name(string)
        google(name)
    elif re.search(r".*note.*", string):
        makeNote()
    elif string == "add website":
        addWebsite()
    elif string == "exit":
        print("Ok, goodbye! :)")
        exit(0)
    else:
        print("I don't know this command")

print("Hello, how can I help you?")
while True:
    command = getInput()
    check_command(command)