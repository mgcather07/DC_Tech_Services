# locations.py
from webex_bot.models.command import Command
from webex_bot.models.response import Response

class LocationsCommand(Command):
    def __init__(self):
        super().__init__(
            command_keyword="locations",
            help_message="Shows the locations adaptive card",
            card=None
        )

    def execute(self, message, attachment_actions, activity):
        adaptive_card = {
            "type": "AdaptiveCard",
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.2",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Drummond Locations",
                    "wrap": True,
                    "size": "Medium",
                    "weight": "Bolder"
                },
                {
                    "type": "TextBlock",
                    "text": "Enter location name:",
                    "wrap": True,
                    "size": "Small"
                },
                {
                    "type": "Input.Text",
                    "placeholder": "Location"
                },
                {
                    "type": "ActionSet",
                    "actions": [
                        {
                            "type": "Action.Submit",
                            "title": "Submit",
                            "style": "positive",
                            "data": {
                                "callback_keyword": "locations"
                            }
                        }
                    ]
                }
            ]
        }

        return Response(
            text="Here is your adaptive card",
            attachments=[adaptive_card]
        )
