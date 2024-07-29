import os
import logging
from webex_bot.webex_bot import WebexBot
from webex_bot.commands.echo import EchoCommand
from webex_bot.commands.help import HelpCommand
from location import Location


# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Set Webex API key as the WEBEX_TOKEN environment variable &
# we'll retrieve that here:
webex_token = os.environ["WEBEX_ACCESS_TOKEN"]

# Create an instance of the Webex bot
bot = WebexBot(webex_token)

# Register custom commands with the bot
location_command = Location()

# Add commands to the bot
bot.add_command(location_command)
bot.add_command(EchoCommand())


# Connect to Webex & start bot listener
bot.run()
