import json
import logging
from webex_bot.models.command import Command
from webex_bot.models.response import Response
from adaptivecardbuilder import AdaptiveCard, TextBlock, FactSet, Fact

log = logging.getLogger(__name__)

with open("./input-card.json", "r") as card:
    INPUT_CARD = json.load(card)

class Location(Command):
    def __init__(self):
        # Define custom command info here
        super().__init__(
            command_keyword="location",
            help_message="Drummond locations",
            card=INPUT_CARD,
        )

    def execute(self, message, attachment_actions, activity):
        # By default, all incoming input will come from adaptive card submission
        # Will pull 'location' from incoming attachment_actions dictionary
        location_name = attachment_actions.inputs['location']

        # Define dummy data for the location
        location_info = {
            "ABC Coke": {
                "address": "123 Main St, Birmingham, AL",
                "phone": "(205) 555-1234",
                "hours": "Mon-Fri 9am-5pm"
            },
            "XYZ Steel": {
                "address": "456 Industrial Rd, Birmingham, AL",
                "phone": "(205) 555-5678",
                "hours": "Mon-Sat 8am-6pm"
            }
        }

        # Fetch location information
        location_details = location_info.get(location_name, None)
        if not location_details:
            resp = Response()
            resp.text = f"Location '{location_name}' not found."
            return resp

        # Build adaptive card
        card = AdaptiveCard()
        card.add(
            [
                TextBlock(text=f"Location Information for {location_name}", size="Medium", weight="Bolder"),
                FactSet(
                    facts=[
                        Fact(title="Address", value=location_details["address"]),
                        Fact(title="Phone", value=location_details["phone"]),
                        Fact(title="Hours", value=location_details["hours"]),
                    ]
                )
            ]
        )

        # Convert card data to JSON
        card_data = json.loads(card.to_json())

        # Build card response
        response = Response()
        # Fallback text
        response.text = "Location information card"
        # Attachments being sent to user
        response.attachments = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card_data,
        }

        return response
