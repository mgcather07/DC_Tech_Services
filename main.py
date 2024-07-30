import os
import logging
from webex_bot.webex_bot import WebexBot
from webex_bot.commands.echo import EchoCommand
from Commands.location import Location
from Commands.servers import Servers, run_scheduler

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Set Webex API key as the WEBEX_TOKEN environment variable &
# we'll retrieve that here:
webex_token = os.environ["WEBEX_ACCESS_TOKEN"]

# Define approved users, domains, and rooms
approved_users = ["MCather@drummondco.com"]

# Create an instance of the Webex bot with approved parameters
bot = WebexBot(
    teams_bot_token=webex_token,
    approved_users=approved_users
)

# Register custom commands with the bot
location_command = Location()
servers_command = Servers(access_token=webex_token)

# Add commands to the bot
bot.add_command(location_command)
bot.add_command(servers_command)
bot.add_command(EchoCommand())

# Start the server status scheduler
run_scheduler(access_token=webex_token)

# Connect to Webex & start bot listener
bot.run()
