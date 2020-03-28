import msvcrt
import sys
import requests
import config
from datetime import datetime
from termcolor import colored, cprint
import json
import pyttsx3
import time


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
    command = input()
    return command


# Declare method to close program
def exitLuna():
    lunaSay("Exiting...")
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
    ttsEngine.setProperty("volume", 0.4)

    # Changing Luna's rate
    rate = ttsEngine.getProperty("rate")
    ttsEngine.setProperty("rate", rate + 50)

    # Say and print Luna's message
    cprint(text, "magenta")
    ttsEngine.say(text)
    ttsEngine.runAndWait()


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
    if command.__contains__("turn off") and command.__contains__("lights"):
        lifx.turnOff()
    elif command.__contains__("turn on") and command.__contains__("lights"):
        lifx.turnOn()
    elif command.__contains__("time") or command.__contains__("date"):
        lunaSay(getDate())
    elif command.startswith("no") or command.startswith("close") or command.startswith("exit"):
        exitLuna()
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
    elif command.__contains__("weather"):
        if command.__contains__("today"):
            weather.currentWeather()
    else:
        lunaSay("I'm sorry, I don't understand.")

    # Re ask
    main()


# Start the program
main()
