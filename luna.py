import sys

import requests
import config


# Create LIFX class
class lifx:
    # Declare LIFX token
    token = config.lifxToken

    # Declare turn off method
    @staticmethod
    def turnOff():
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

# Declare method to get command from user
def getCommand():
    # Get input
    command = input()
    return command

# Declare method to close program
def exitLuna():
    print("Exiting...")
    sys.exit(0)

# Declare main loop
def main():

    # Display message
    if config.firstBoot:
        config.firstBoot = False
        print("Hi! I'm Luna! How may I be of service today:")
    else:
        print("Anything else?")

    # Get command from user
    command = getCommand().lower()

    # Parse command
    if command.__contains__("turn off my lights"):
        lifx.turnOff()
    elif command.__contains__("turn on my lights"):
        lifx.turnOn()
    elif command.startswith("no"):
        exitLuna()

    # Re ask
    main()

# Start the program
main()
