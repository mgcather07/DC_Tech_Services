import os
import logging
from webex_bot.webex_bot import WebexBot
from location import Location

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Set Webex API key as the WEBEX_TOKEN environment variable &
# we'll retrieve that here:
webex_token = os.environ["WEBEX_ACCESS_TOKEN"]

# Define approved users
approved_users = ['MCather@drummondco.com']


# Overriding the WebexBot class to add logging for user checks
class CustomWebexBot(WebexBot):
    def __init__(self, access_token, **kwargs):
        super().__init__(access_token, **kwargs)

    def on_message(self, message):
        user_email = message.personEmail
        log.info(f"Incoming message from {user_email}")

        if user_email in self.approved_users:
            log.info(f"User {user_email} is approved.")
            super().on_message(message)
        else:
            log.warning(f"User {user_email} is not approved.")
            response = "You are not authorized to use this bot."
            self.teams.messages.create(roomId=message.roomId, text=response)


# Create an instance of the custom bot
custom_bot = CustomWebexBot(webex_token, approved_users=approved_users)

# Register custom command with the bot
custom_bot.add_command(Location())

# Connect to Webex & start bot listener
custom_bot.run()
