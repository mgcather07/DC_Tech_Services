# main.py
from webex_bot.webex_bot import WebexBot
import os
from locations import LocationsCommand

# Get the Webex access token from environment variables
access_token = os.getenv('WEBEX_ACCESS_TOKEN')

# Initialize the bot with the access token
bot = WebexBot(access_token)

# Register the Locations command
locations_command = LocationsCommand()
bot.add_command(locations_command)

# Run the bot
bot.run()
