import json
import logging
import subprocess
import schedule
import time
from webex_bot.models.command import Command
from webex_bot.models.response import Response
from webexteamssdk import WebexTeamsAPI

log = logging.getLogger(__name__)

class Servers(Command):
    def __init__(self, access_token, room_id, db_connection=None):
        super().__init__(
            command_keyword="servers",
            help_message="Check the status of Cisco servers",
            card=None,  # Handle card creation in the execute method or adapt to new style
        )
        self.server_addresses = {
            "publisher": "10.0.10.200",
            "abc_admin": "192.168.1.101"
        }
        self.server_status = {server: "Unknown" for server in self.server_addresses}
        self.webex_api = WebexTeamsAPI(access_token=access_token)
        self.room_id = room_id
        self.db_connection = db_connection  # Store db_connection if needed
        log.info("Servers command initialized.")

    def execute(self, message, attachment_actions, activity):
        server_name = attachment_actions.inputs['server']
        log.info(f"Received request to check status of server: {server_name}")

        server_address = self.server_addresses.get(server_name, None)
        if not server_address:
            resp = Response()
            resp.text = f"Server '{server_name}' not found."
            log.warning(f"Server '{server_name}' not found.")
            return resp

        status = self.ping_server(server_address)

        response_text = f"Server: {server_name}\nStatus: {status}"

        response = Response()
        response.text = response_text

        log.info(f"Status of server '{server_name}': {status}")
        return response

    def ping_server(self, server_address):
        try:
            log.info(f"Pinging server {server_address}")
            output = subprocess.run(["ping", "-c", "1", server_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if output.returncode == 0:
                log.info(f"Server {server_address} is online")
                return "Online"
            else:
                log.info(f"Server {server_address} is offline")
                return "Offline"
        except Exception as e:
            log.error(f"Error pinging server {server_address}: {e}")
            return "Error checking status"

    def check_servers(self):
        log.info("Checking server statuses.")
        for server_name, server_address in self.server_addresses.items():
            current_status = self.ping_server(server_address)
            log.info(f"Status of server '{server_name}' ({server_address}): {current_status}")
            if current_status != self.server_status[server_name]:
                self.server_status[server_name] = current_status
                if current_status == "Offline":
                    self.send_alert(server_name, server_address, current_status)

    def send_alert(self, server_name, server_address, status):
        message = f"Alert: '{server_name}' ({server_address}) is {status}."
        log.info(f"Sending alert: {message}")
        self.webex_api.messages.create(roomId=self.room_id, text=message)

def run_scheduler(access_token, room_id):
    servers = Servers(access_token=access_token, room_id=room_id)
    schedule.every(15).minutes.do(servers.check_servers)
    log.info("Scheduler started.")
    while True:
        log.debug("Running scheduled tasks...")
        schedule.run_pending()
        time.sleep(1)
