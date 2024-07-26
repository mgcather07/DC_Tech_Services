from webex_bot.webex_bot import WebexBot
import os
from switch import Switch  # Import the Switch command from switch.py

# Get the Webex access token from environment variables
access_token = os.getenv('WEBEX_ACCESS_TOKEN')

# Initialize the bot with the access token
bot = WebexBot(access_token)

# Add the Switch command to the bot
switch_command = Switch()
bot.add_command(switch_command)

# Run the bot
bot.run()
