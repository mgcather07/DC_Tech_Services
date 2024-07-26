from webex_bot.models.command import Command


class Switch(Command):
    def __init__(self):  # Fixing the typo __int__ to __init__
        super().__init__(
            command_keyword="switch",
            help_message="Get current switch information",
            card=None,
        )

    def execute(self, message, attachment_actions, activity):
        return f"Pythong King is doing work! {message}"