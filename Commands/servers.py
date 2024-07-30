import json
import logging
import subprocess
import schedule
import time
import os
from webex_bot.models.command import Command
from webex_bot.models.response import Response
from webexteamssdk import WebexTeamsAPI

log = logging.getLogger(__name__)

# Get the current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the absolute path to the servers-card.json file
card_path = os.path.join(current_dir, "servers-card.json")

log.info(f"Card path: {card_path}")

try:
    with open(card_path, "r") as card:
        SERVERS_CARD = json.load(card)
        log.info("Loaded servers-card.json successfully.")
except FileNotFoundError:
    log.error(f"File not found: {card_path}")
    raise

class Servers(Command):
    def __init__(self, access_token):
        super().__init__(
            command_keyword="servers",
            help_message="Check the status of Cisco servers",
            card=SERVERS_CARD,
        )
        self.server_addresses = {
            "unraid": "192.168.10.10",
            "server2": "192.168.1.2",
            "server3": "192.168.1.3"
        }
        self.server_status = {server: "Unknown" for server in self.server_addresses}
        self.webex_api = WebexTeamsAPI(access_token=access_token)
        log.info("Servers command initialized.")

    def execute(self, message, attachment_actions, activity):
        server_name = attachment_actions.inputs['server']
        log.info(f"Received request to check status of server: {server_name}")

        # Fetch server address
        server_address = self.server_addresses.get(server_name, None)
        if not server_address:
            resp = Response()
            resp.text = f"Server '{server_name}' not found."
            log.warning(f"Server '{server_name}' not found.")
            return resp

        # Perform ping
        status = self.ping_server(server_address)

        # Prepare text response
        response_text = f"Server: {server_name}\nStatus: {status}"

        # Build text response
        response = Response()
        response.text = response_text

        log.info(f"Status of server '{server_name}': {status}")
        return response

    def ping_server(self, server_address):
        """
        Ping the server to check its status.
        """
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
        """
        Check the status of all servers and send alerts if any server goes offline.
        """
        log.info("Checking server statuses.")
        for server_name, server_address in self.server_addresses.items():
            current_status = self.ping_server(server_address)
            log.info(f"Status of server '{server_name}' ({server_address}): {current_status}")
            if current_status != self.server_status[server_name]:
                self.server_status[server_name] = current_status
                if current_status == "Offline":
                    self.send_alert(server_name, server_address, current_status)

    def send_alert(self, server_name, server_address, status):
        """
        Send an alert via Webex.
        """
        message = f"Alert: Server '{server_name}' ({server_address}) is {status}."
        log.info(f"Sending alert: {message}")
        self.webex_api.messages.create(roomId='Y2lzY29zcGFyazovL3VzL1JPT00vMGYwN2EyZjAtNGI2YS0xMWVmLWI4N2MtNTdhYTcwOWRhMGU1', text=message)

def run_scheduler(access_token):
    servers = Servers(access_token)
    schedule.every(5).seconds.do(servers.check_servers)
    log.info("Scheduler started.")
    while True:
        log.debug("Running scheduled tasks...")
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
