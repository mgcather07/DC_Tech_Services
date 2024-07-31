import os
import json
import logging
import threading
from webex_bot.webex_bot import WebexBot
from webex_bot.commands.echo import EchoCommand
from Commands.location import Location
from Commands.servers import Servers, run_scheduler
from SQL.db_connection import connect_to_sql_server

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Set Webex API key as the WEBEX_TOKEN environment variable & we'll retrieve that here:
webex_token = os.environ["WEBEX_ACCESS_TOKEN"]

# Correct room ID where you want to send alerts
room_id = os.environ["WEBEX_ROOM_ID"]

# Load approved users from JSON file
def load_approved_users(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['approved_users']

# Use the correct path to the JSON file
approved_users_file = os.path.join(os.path.dirname(__file__), 'Utils', 'approved_users.json')
approved_users = load_approved_users(approved_users_file)

# Initialize the database connection
db_connection = connect_to_sql_server()
if db_connection is None:
    log.error("Failed to establish database connection. Exiting.")
    exit(1)

# Create an instance of the Webex bot with approved parameters
bot = WebexBot(
    teams_bot_token=webex_token,
    approved_users=approved_users
)

# Register custom commands with the bot
location_command = Location()
servers_command = Servers(access_token=webex_token, room_id=room_id, db_connection=db_connection)

# Add commands to the bot
bot.add_command(location_command)
bot.add_command(servers_command)
bot.add_command(EchoCommand())

# Function to run the scheduler in a separate thread
def start_scheduler():
    run_scheduler(access_token=webex_token, room_id=room_id, db_connection=db_connection)

# Create and start the scheduler thread
scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
scheduler_thread.start()

# Connect to Webex & start bot listener
bot.run()
