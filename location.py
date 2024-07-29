import json
import logging
from webex_bot.models.command import Command
from webex_bot.models.response import Response

log = logging.getLogger(__name__)

with open("./input-card.json", "r") as card:
    INPUT_CARD = json.load(card)

class Location(Command):
    def __init__(self):
        # Define custom command info here
        super().__init__(
            command_keyword="location",
            help_message="Locations",
            card=INPUT_CARD,
        )

    def execute(self, message, attachment_actions, activity):
        # By default, all incoming input will come from adaptive card submission
        # Will pull 'location' from incoming attachment_actions dictionary
        location_name = attachment_actions.inputs['location']

        # Define dummy data for the location
        location_info = {
            "ABC Coke": {
                "address": "900 Huntsville Ave, Birmingham, AL 35217",
                "contact": "Scott Castleberry",
                "external_extension": "(205) 849-1377",
                "internal_extension": "7377"
            },
            "Hangar": {
                "address": "3800 65th St N, Birmingham, AL 35206",
                "contact": "Misty Estes",
                "external_extension": "(205) 917-3133",
                "internal_extension": "3133"
            }
        }

        # Fetch location information
        location_details = location_info.get(location_name, None)
        if not location_details:
            resp = Response()
            resp.text = f"Location '{location_name}' not found."
            return resp

        # Prepare text response
        response_text = f"{location_name}\n"
        response_text += f"Address: {location_details['address']}\n"
        response_text += f"Contact: {location_details['contact']}\n"
        response_text += f"External Extension: {location_details['external_extension']}\n"
        response_text += f"Internal Extension: {location_details['internal_extension']}"

        # Build text response
        response = Response()
        response.text = response_text

        return response