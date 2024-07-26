import os

from webex_bot.webex_bot import WebexBot

from weather import Location

# Set Webex API key as the WEBEX_TOKEN environment variable &
# we'll retrieve that here:
webex_token = os.environ["WEBEX_ACCESS_TOKEN"]

# Bot only needs the Webex token, but optionally we can also
# restrict who the bot will respond to by user or domain.
# For example:
WebexBot(webex_token, approved_users=['mcather@drummondco.com'])
# Restrict by domain: WebexBot(webex_token, approved_domains=['example.local'])
bot = WebexBot(webex_token)

# Registed custom command with the bot:
bot.add_command(Location())

# Connect to Webex & start bot listener:
bot.run()