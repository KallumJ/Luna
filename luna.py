import sys
import requests
import config
from datetime import datetime
from termcolor import colored, cprint
import json

# Create LIFX class
class lifx:
    # Declare LIFX token
    token = config.lifxToken

    # Declare turn off method
    @staticmethod
    def turnOff():
        # Print response
        cprint("Turning off the lights...", "magenta")

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
        cprint("Turning on the lights...", "magenta")

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
        cprint("Changing colour of lights to " + colour + "...", "magenta")

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

class weather:

    @staticmethod
    def currentWeather():
        # Find city
        ipData = requests.get("https://api.ipdata.co/?api-key=" + config.ipDataKey).json()
        city = ipData["city"]

        # Request current weather information
        cWeather = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + config.openWeatherKey)

        # Store weather information
        cWeatherJSON = json.loads(cWeather.text)

        # Parse current weather
        cWeatherDict = cWeatherJSON["weather"]
        cWeatherDesc = cWeatherDict[0].get("description")

        # Parse current temperature
        cWeatherMain = cWeatherJSON["main"]
        cWeatherTemp = str(round(cWeatherMain.get("temp") - 273.15))

        # Print reponse
        cprint("The weather in " + city + " is " + cWeatherDesc + " with a temperature of " + cWeatherTemp + chr(176) + "C", "magenta")

# Declare method to get command from user
def getCommand():
    # Get input
    command = input()
    return command


# Declare method to close program
def exitLuna():
    cprint("Exiting...", "magenta")
    sys.exit(0)


def getDate():
    time = datetime.now().time().strftime("%H:%M")
    date = datetime.today().strftime("%d/%m/%Y")

    return "The time is: " + time + " on the " + date


# Declare main loop
def main():
    # Display message
    if config.firstBoot:
        config.firstBoot = False
        cprint("Hi! I'm Luna! How may I be of service today:", "magenta")
    else:
        cprint("Anything else?", "magenta")

    # Get command from user
    command = getCommand().lower()

    # Parse command
    if command.__contains__("turn off") and command.__contains__("lights"):
        lifx.turnOff()
    elif command.__contains__("turn on") and command.__contains__("lights"):
        lifx.turnOn()
    elif command.__contains__("time") or command.__contains__("date"):
        cprint(getDate(), "magenta")
    elif command.startswith("no") or command.startswith("close") or command.startswith("exit"):
        exitLuna()
    elif command.__contains__("colour") or command.__contains__("color") or command.__contains__("set") and command.__contains__("lights"):
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
        cprint("I'm sorry, I don't understand.", "magenta")

    # Re ask
    main()

# Start the program
main()
