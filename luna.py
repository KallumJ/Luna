import os
import sys
import requests
import config
from datetime import datetime
from termcolor import colored, cprint
import json
import pyttsx3
import html
import vlc
import random
from mutagen.easyid3 import EasyID3
import feedparser


# Create LIFX class
class lifx:
    # Declare LIFX token
    token = config.lifxToken

    # Declare turn off method
    @staticmethod
    def turnOff():
        # Print response
        lunaSay("Turning off the lights...")

        # Give authorisation
        headers = {
            "Authorization": "Bearer %s" % lifx.token,
        }

        # Issue commmand to turn off
        payload = {
            "power": "off",
        }

        # Send request
        response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)

    # Declare turn on method
    @staticmethod
    def turnOn():
        # Print response
        lunaSay("Turning on the lights...")

        # Give authorisation
        headers = {
            "Authorization": "Bearer %s" % lifx.token,
        }

        # Issue commmand to turn on
        payload = {
            "power": "on",
        }

        # Send request
        response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)

    @staticmethod
    def setColour(colour):
        # Print response
        lunaSay("Changing colour of lights to " + colour + "...")

        # Give authorisation
        headers = {
            "Authorization": "Bearer %s" % lifx.token,
        }

        # Issue commmand to turn off
        payload = {
            "power": "on",
            "color": colour,
        }

        # Send request
        response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)

    @staticmethod
    def flash(colour):
        lunaSay("Flashing lights " + colour)

        headers = {
            "Authorization": "Bearer %s" % lifx.token,
        }

        data = {
            "period": 0.5,
            "cycles": 30,
            "color": colour
        }

        response = requests.post('https://api.lifx.com/v1/lights/all/effects/pulse', data=data, headers=headers)


# Create weather class
class weather:

    # Method to return current weather information in your area
    @staticmethod
    def currentWeather():
        # Find city
        ipData = requests.get("https://api.ipdata.co/?api-key=" + config.ipDataKey).json()
        city = ipData["city"]

        # Request current weather information
        cWeather = requests.get(
            "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + config.openWeatherKey)

        # Store weather information
        cWeatherJSON = json.loads(cWeather.text)

        # Parse current weather
        cWeatherDict = cWeatherJSON["weather"]
        cWeatherDesc = cWeatherDict[0].get("description")

        # Parse current temperature
        cWeatherMain = cWeatherJSON["main"]
        cWeatherTemp = str(round(cWeatherMain.get("temp") - 273.15))

        # Print reponse
        lunaSay("The weather in " + city + " is " + cWeatherDesc + " with a temperature of " + cWeatherTemp + chr(
            176) + "C")


# Declare method to get command from user
def getCommand():
    # Get input
    command = input().lower()
    return command


# Declare method to close program
def exitLuna():
    lunaSay("Exiting... Goodbye")
    sys.exit(0)


# Declare method to return the current date
def getDate():
    time = datetime.now().time().strftime("%H:%M")
    date = datetime.today().strftime("%d/%m/%Y")

    return "The time is: " + time + " on the " + date


# Declare method to allow Luna to talk
def lunaSay(text):
    # Initalise tts engine
    ttsEngine = pyttsx3.init()

    # Set Luna's vocie
    voices = ttsEngine.getProperty("voices")
    ttsEngine.setProperty("voice", voices[1].id)

    # Set Luna's volume
    ttsEngine.setProperty("volume", 0.6)

    # Changing Luna's rate
    rate = ttsEngine.getProperty("rate")
    ttsEngine.setProperty("rate", rate + 50)

    # Say and print Luna's message
    cprint(text, "magenta")
    ttsEngine.say(text)
    ttsEngine.runAndWait()


# Declare method to play trivia
def trivia():
    # Get response
    response = requests.get("https://opentdb.com/api.php?amount=1")

    # Create json
    triviaJSON = json.loads(response.text)

    # Parse question and answer
    triviaDict = triviaJSON["results"]
    triviaQ = html.unescape(triviaDict[0].get("question"))
    triviaA = html.unescape(str(triviaDict[0].get("correct_answer"))).lower()

    # Read trivia question
    lunaSay(triviaQ)

    # Read in answer
    userAnswer = input("Answer:")
    userAnswer = userAnswer.lower()

    # Check answer is correct
    if triviaA == userAnswer:
        lunaSay("Correct! Well done!")
    else:
        lunaSay("Incorrect! Better luck next time!")

    # Keep asking user to play again until they say no
    response = True
    while response:

        lunaSay("Would you like to play again?")

        answer = getCommand()

        if answer.lower() == "yes" or answer.lower() == "y":
            response = False
            trivia()
        elif answer.lower() == "no" or answer.lower() == "n":
            response = False
            return
        else:
            response = True


# Declare method to play music
def music(directory, shuffle):
    # TODO Doesn't continue playing song
    # TODO Invalid sample rate issues

    songs = []

    # Create array of all the songs in the directory
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            songs.append(directory + "/" + file)

    # If no valid songs are found, return error
    if not songs:
        lunaSay("No .mp3 files found")
        return

    # If shuffle is required, randomise the array
    if shuffle:
        random.shuffle(songs)

    # Create vlc instance
    instance = vlc.Instance()
    player = instance.media_player_new()

    # While there are songs left to play
    i = 0
    while i != len(songs):
        # Set vlc media to the current song
        media = instance.media_new(songs[i])
        player.set_media(media)

        # Get mp3 metadata
        audio = EasyID3(songs[i])

        # Print current song being played
        cprint("Now playing: " + audio["title"][0] + " - " + audio["artist"][0], "magenta")

        # Play the song
        player.play()

        # While command is not to move to new song
        new = False
        while not new:

            # Print message
            cprint("Let me know if you want the next track, the previous track, or to pause or play, or stop",
                   "magenta")

            # Get command
            command = getCommand()

            # If command is to pause
            if command.__contains__("pause"):
                player.pause()
                lunaSay("Pausing...")

            # If command is to play
            elif command.__contains__("play"):
                cprint("Playing...", "magenta")
                player.play()

            # If command is to go to next track
            elif command.__contains__("next"):
                i = i + 1
                new = True
                continue

            # If command is to go to previous track
            elif command.__contains__("previous"):
                i = i - 1
                new = True

            # If command is to stop playing music
            elif command.__contains__("stop"):
                player.stop()
                return

            # If command is not recognised
            else:
                cprint("I don't understand. Please please try again", "magenta")


# Declare method to play podcast
def podcast(pod):
    # Declare dictionary of podcasts
    podcasts = {
        "triforce": "http://yogpod.libsyn.com/rss",
        "truegeordie": "https://audioboom.com/channels/4902377.rss"
    }

    # Parse required podcast
    if str(pod).__contains__("tri"):
        # GET TRIFORCE URL

        # Parse link
        triforce = feedparser.parse(podcasts.get("triforce"))

        # Find number of entires
        numOfEntries = len(triforce.entries)

        # Read in the entry
        entry = triforce.entries[random.randint(1, numOfEntries - 85)]

        # Find the url
        url = entry.enclosures[0].get("href")

    elif str(pod).__contains__("true"):
        # GET TG URL
        # Parse link
        tg = feedparser.parse(podcasts.get("truegeordie"))

        # Find number of entries
        numOfEntries = len(tg.entries)

        # Read in the entry
        entry = tg.entries[random.randint(1, numOfEntries)].enclosures

        # Find the URL
        url = entry[0].get("href")

    # Play the media
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(url)
    media.get_mrl()
    player.set_media(media)
    lunaSay("Playing podcast!")
    player.play()

    # While no response to stop is given
    valid = False
    while not valid:
        cprint("Let me know when to whether to pause, play, or stop the podcast", "magenta")

        command = getCommand()

        if command.__contains__("stop"):
            player.stop()
            lunaSay("Stopping podcast...")
            valid = True
        elif command.__contains__("pause"):
            player.pause()
            lunaSay("Pausing...")
        elif command.__contains__("play") or command.__contains__("resume"):
            player.play()
        else:
            lunaSay("I do not understand")


# Declare main loop
def main():
    # Prompt for input
    if config.firstBoot:
        config.firstBoot = False
        lunaSay("Hi! I'm Luna! How may I be of service today")
    else:
        lunaSay("Anything else?")

    # Get command from user
    command = getCommand().lower()

    # Parse command
    # Turn off lights
    if command.__contains__("turn off") and command.__contains__("lights"):
        lifx.turnOff()

    # Turn on lights
    elif command.__contains__("turn on") and command.__contains__("lights"):
        lifx.turnOn()

    # Get time
    elif command.__contains__("time") or command.__contains__("date"):
        lunaSay(getDate())

    # Close program
    elif command.startswith("no") or command.startswith("close") or command.startswith("exit") or command.startswith(
            "goodbye"):
        exitLuna()

    # Change light colour
    elif command.__contains__("colour") or command.__contains__("color") or command.__contains__(
            "set") and command.__contains__("lights"):
        if command.__contains__("pink"):
            lifx.setColour("pink")
        elif command.__contains__("blue"):
            lifx.setColour("blue")
        elif command.__contains__("red"):
            lifx.setColour("red")
        elif command.__contains__("orange"):
            lifx.setColour("orange")
        elif command.__contains__("green"):
            lifx.setColour("green")
        elif command.__contains__("yellow"):
            lifx.setColour("yellow")
        elif command.__contains__("purple"):
            lifx.setColour("purple")
        elif command.__contains__("white"):
            lifx.setColour("white")

    # Flash lights
    elif command.__contains__("lights") and command.__contains__("flash"):

        # Re ask until colour found
        valid = False
        while not valid:
            lunaSay("What colour would you like to flash the lights?")

            answer = getCommand()

            if answer.__contains__("not") or answer.__contains__("don't") or answer.__contains__(
                    "dont") or answer.__contains__("no"):
                valid = True
                lunaSay("Aborting flash operation...")
            elif answer.__contains__("pink") or answer.__contains__("blue") or answer.__contains__(
                    "red") or answer.__contains__("orange") or answer.__contains__("green") or answer.__contains__(
                "yellow") or answer.__contains__("purple") or answer.__contains__("white"):
                valid = True
                lifx.flash(answer)
            else:
                lunaSay("I'm sorry. I don't recognise that colour")

    # Get weather
    elif command.__contains__("weather") or command.__contains__("temperature"):

        # If inital command says when
        if command.__contains__("today"):
            weather.currentWeather()
        elif command.__contains__("week"):
            lunaSay("Weekly weather forecasting is not yet available")
        else:
            # Re ask until timeframe is established
            valid = False
            while not valid:
                lunaSay("Would you like to know the weather today, or for the week?")

                answer = getCommand()
                if answer.__contains__("today"):
                    valid = True
                    weather.currentWeather()
                elif answer.__contains__("week"):
                    valid = True
                    lunaSay("Weekly weather forecasting is not yet available")
                elif answer.__contains__("no") or answer.__contains__("cancel"):
                    valid = True
                    lunaSay("Cancelling...")
                else:
                    lunaSay("I'm sorry, I dont understand")

    # Asked name
    elif command.__contains__("your") and command.__contains__("name"):
        lunaSay("My name is Luna! Nice to meet you :)")

    # Play trivia
    elif command.__contains__("trivia"):
        trivia()

    # Play music
    elif command.__contains__("music") or command.__contains__("song"):
        # TODO Regular Expressions on File Directory

        # While no valid response is given
        valid = False
        while not valid:

            # Ask for file path
            lunaSay("Please specify the file path to where your music is located")
            directory = getCommand()

            # If file path is empty
            if not directory:
                lunaSay("I don't understand this directory.")
            else:
                valid = True

        # While no valid response is given
        valid = False
        while not valid:

            # Ask if they are to shuffle
            lunaSay("Would you like to shuffle?")
            shuffle = getCommand()

            # Parse response
            if shuffle.__contains__("yes") or shuffle == "y":
                valid = True
                music(directory, shuffle=True)
            elif shuffle.__contains__("no") or shuffle == "n":
                valid = True
                music(directory, shuffle=False)
            else:
                lunaSay("I do not understand.")

    # Play podcast
    elif command.__contains__("podcast"):

        # While no valid response is given
        valid = False
        while not valid:
            lunaSay("What podcast would you like?")

            pod = getCommand()

            if pod.__contains__("tri"):
                valid = True
                podcast("tri")
            elif pod.__contains__("true"):
                valid = True
                podcast("true")
            elif pod.__contains__("cancel"):
                valid = True
            else:
                lunaSay("I do not understand.")

    # Did not understand
    else:
        lunaSay("I'm sorry, I don't understand.")

    # Re ask
    main()


# Start the program
main()
