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
import feedparser
import os
from mutagen.easyid3 import EasyID3


# Create LIFX class
class lifx:
    # Declare LIFX token
    token = config.lifxToken

    # Declare turn off method
    @staticmethod
    def turnOff():
        # Print response
        luna.lunaSay("Turning off the lights...")

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
        luna.lunaSay("Turning on the lights...")

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
        luna.lunaSay("Changing colour of lights to " + colour + "...")

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
        luna.lunaSay("Flashing lights " + colour)

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
        luna.lunaSay("The weather in " + city + " is " + cWeatherDesc + " with a temperature of " + cWeatherTemp + chr(
            176) + "C")


# Create Luna class
class luna:

    # Declare method to get command from user
    @staticmethod
    def getCommand():
        # Get input
        command = input().lower()
        return command

    # Declare method to close program
    @staticmethod
    def exitLuna():
        luna.lunaSay("Exiting... Goodbye")
        sys.exit(0)

    # Declare method to allow Luna to talk
    @staticmethod
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
        os.system("cls")
        print("|                                         |")
        print("|       .                      .          |")
        print("|                                         |")
        print("|                                         |")
        print("|                                         |")
        print("|     |                         |         |")
        print("|     |_________________________|         |")
        print("|                                         |")
        print("|                                         |")
        print("                                           ")

        cprint(text, "magenta")
        ttsEngine.say(text)
        ttsEngine.runAndWait()


# Create class for general util methods
class util:

    # Declare method to return the current date
    @staticmethod
    def getDate():
        time = datetime.now().time().strftime("%H:%M")
        date = datetime.today().strftime("%d/%m/%Y")

        return "The time is: " + time + " on the " + date


# Create games class
class games:
    # Declare method to play trivia
    @staticmethod
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
        luna.lunaSay(triviaQ)

        # Read in answer
        userAnswer = input("Answer:")
        userAnswer = userAnswer.lower()

        # Check answer is correct
        if triviaA == userAnswer:
            luna.lunaSay("Correct! Well done!")
        else:
            luna.lunaSay("Incorrect! Better luck next time!")

        # Keep asking user to play again until they say no
        response = True
        while response:

            luna.lunaSay("Would you like to play again?")

            answer = luna.getCommand()

            if answer.lower() == "yes" or answer.lower() == "y":
                response = False
                games.trivia()
            elif answer.lower() == "no" or answer.lower() == "n":
                response = False
                return
            else:
                response = True


# Create class for all audio features
class audio:

    # Declare method to play podcast
    @staticmethod
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
        luna.lunaSay("Playing podcast!")
        player.play()

        # While no response to stop is given
        valid = False
        while not valid:
            cprint("Let me know when to whether to pause, play, or stop the podcast", "magenta")

            command = luna.getCommand()

            if command.__contains__("stop"):
                player.stop()
                luna.lunaSay("Stopping podcast...")
                valid = True
            elif command.__contains__("pause"):
                player.pause()
                luna.lunaSay("Pausing...")
            elif command.__contains__("play") or command.__contains__("resume"):
                player.play()
            else:
                luna.lunaSay("I do not understand")

    @staticmethod
    def playMusic(directory, shuffle):
        # TODO Doesn't continue playing song
        # TODO Invalid sample rate issues

        songs = []

        # Create array of all the songs in the directory
        for file in os.listdir(directory):
            if file.endswith(".mp3"):
                songs.append(directory + "/" + file)

        # If no valid songs are found, return error
        if not songs:
            luna.lunaSay("No .mp3 files found")
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
                command = luna.getCommand()

                # If command is to pause
                if command.__contains__("pause"):
                    player.pause()
                    luna.lunaSay("Pausing...")

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


# Create class for to do features
class toDo:
    # TODO: Deleting item
    # TODO: Accept remove as input

    @staticmethod
    def addToDo(item):
        with open("todo.json") as infile:
            data = json.load(infile)
            data["todo"].append(item)

        with open("todo.json", "w") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

        luna.lunaSay("Item added to your to do list")

    @staticmethod
    def readToDo():
        with open("todo.json") as jsonFile:
            data = json.load(jsonFile)

            for item in data["todo"]:
                luna.lunaSay(item)

    @staticmethod
    def delToDo(item):
        with open("todo.json") as infile:
            jsonObject = json.load(infile)

            for i in range(len(jsonObject)):
                if jsonObject[i]["todo"] == item:
                    jsonObject.pop(i)
                    break

            open("todo.json", "w").write(json.dumps(jsonObject, ensure_ascii=False, indent=4))

        luna.lunaSay("Item successfully deleted")


# Declare main loop
def main():
    # Prompt for input
    if config.firstBoot:
        config.firstBoot = False
        luna.lunaSay("Hi! I'm Luna! How may I be of service today")
    else:
        luna.lunaSay("Anything else?")

    # Get command from user
    command = luna.getCommand().lower()

    # Parse command
    # Turn off lights
    if command.__contains__("turn off") and command.__contains__("lights"):
        lifx.turnOff()

    # Turn on lights
    elif command.__contains__("turn on") and command.__contains__("lights"):
        lifx.turnOn()

    # Get time
    elif command.__contains__("time") or command.__contains__("date"):
        luna.lunaSay(util.getDate())

    # Close program
    elif command.startswith("no") or command.startswith("close") or command.startswith("exit") or command.startswith(
            "goodbye"):
        luna.exitLuna()

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
            luna.lunaSay("What colour would you like to flash the lights?")

            answer = luna.getCommand()

            if answer.__contains__("not") or answer.__contains__("don't") or answer.__contains__(
                    "dont") or answer.__contains__("no"):
                valid = True
                luna.lunaSay("Aborting flash operation...")
            elif answer.__contains__("pink") or answer.__contains__("blue") or answer.__contains__(
                    "red") or answer.__contains__("orange") or answer.__contains__("green") or answer.__contains__(
                "yellow") or answer.__contains__("purple") or answer.__contains__("white"):
                valid = True
                lifx.flash(answer)
            else:
                luna.lunaSay("I'm sorry. I don't recognise that colour")

    # Get weather
    elif command.__contains__("weather") or command.__contains__("temperature"):

        # If inital command says when
        if command.__contains__("today"):
            weather.currentWeather()
        elif command.__contains__("week"):
            luna.lunaSay("Weekly weather forecasting is not yet available")
        else:
            # Re ask until timeframe is established
            valid = False
            while not valid:
                luna.lunaSay("Would you like to know the weather today, or for the week?")

                answer = luna.getCommand()
                if answer.__contains__("today"):
                    valid = True
                    weather.currentWeather()
                elif answer.__contains__("week"):
                    valid = True
                    luna.lunaSay("Weekly weather forecasting is not yet available")
                elif answer.__contains__("no") or answer.__contains__("cancel"):
                    valid = True
                    luna.lunaSay("Cancelling...")
                else:
                    luna.lunaSay("I'm sorry, I dont understand")

    # Asked name
    elif command.__contains__("your") and command.__contains__("name"):
        luna.lunaSay("My name is Luna! Nice to meet you :)")

    # Play trivia
    elif command.__contains__("trivia"):
        games.trivia()

    # Play music
    elif command.__contains__("music") or command.__contains__("song"):
        # TODO Regular Expressions on File Directory

        # While no valid response is given
        valid = False
        while not valid:

            # Ask for file path
            luna.lunaSay("Please specify the file path to where your music is located")
            directory = luna.getCommand()

            # If file path is empty
            if not directory:
                luna.lunaSay("I don't understand this directory.")
            else:
                valid = True

        # While no valid response is given
        valid = False
        while not valid:

            # Ask if they are to shuffle
            luna.lunaSay("Would you like to shuffle?")
            shuffle = luna.getCommand()

            # Parse response
            if shuffle.__contains__("yes") or shuffle == "y":
                valid = True
                audio.playMusic(directory, shuffle=True)
            elif shuffle.__contains__("no") or shuffle == "n":
                valid = True
                audio.playMusic(directory, shuffle=False)
            else:
                luna.lunaSay("I do not understand.")

    # Play podcast
    elif command.__contains__("podcast"):

        # While no valid response is given
        valid = False
        while not valid:
            luna.lunaSay("What podcast would you like?")

            pod = luna.getCommand()

            if pod.__contains__("tri"):
                valid = True
                audio.podcast("tri")
            elif pod.__contains__("true"):
                valid = True
                audio.podcast("true")
            elif pod.__contains__("cancel"):
                valid = True
            else:
                luna.lunaSay("I do not understand.")

    elif command.__contains__("to") and command.__contains__("do"):
        valid = False
        while not valid:
            luna.lunaSay(
                "Would you like me to add something to your to do list, remove something or read out the list?")

            answer = luna.getCommand()

            if answer.__contains__("add"):

                luna.lunaSay("What would you like to add?")
                item = luna.getCommand()
                toDo.addToDo(item)

                valid = True
            elif answer.__contains__("read"):
                toDo.readToDo()

                valid = True
            elif answer.__contains__("del"):

                luna.lunaSay("What item would you like to delete?")

                item = luna.getCommand()

                toDo.delToDo(item)

            else:
                luna.lunaSay("I'm sorry. I do not understand.")

    # Did not understand
    else:
        luna.lunaSay("I'm sorry, I don't understand.")

    # Re ask
    main()


# Loop through the program
main()
