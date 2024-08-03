# Bot/commands/switch.py

import pymysql
import logging
from Bot.models.command import Command
from Bot.models.response import Response

log = logging.getLogger(__name__)

class Switch(Command):
    def __init__(self, db_connection):
        super().__init__(
            command_keyword="switch",
            help_message="Get information about switches",
            card=None,  # Handle card creation in the execute method or adapt to new style
        )
        self.db_connection = db_connection
        log.info("Switch command initialized.")

    def execute(self, message, attachment_actions, activity):
        log.info("Received request to get switch information.")
        switches = self.get_switch_data()
        if not switches:
            resp = Response()
            resp.text = "No switch data available."
            log.warning("No switch data available.")
            return resp

        response_text = "Switch Data:\n"
        for switch in switches:
            response_text += f"ID: {switch['id']}, Name: {switch['name']}, Model: {switch['model']}, IP Address: {switch['ip_address']}, Location: {switch['location']}, Installed Date: {switch['installed_date']}\n"

        response = Response()
        response.text = response_text

        log.info("Switch data retrieved successfully.")
        return response

    def get_switch_data(self):
        try:
            with self.db_connection.cursor() as cursor:
                sql = "SELECT id, name, model, ip_address, location, installed_date FROM switch_data"
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            log.error(f"Error querying switch data: {e}")
            return None
