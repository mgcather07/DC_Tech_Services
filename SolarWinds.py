from orionsdk import SwisClient
import os
import urllib3

# Suppress HTTPS warnings for testing purposes
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Prompt for the SolarWinds server credentials
solarwinds_server = os.environ["SOLARWINDS_SERVER"]
username = os.environ["SOLARWINDS_USERNAME"]
password = os.environ["SOLARWINDS_PASSWORD"]

# Initialize the client
swis = SwisClient(solarwinds_server, username, password)

def get_switches_with_location():
    query = """
    SELECT 
        n.NodeID,
        n.Caption AS DeviceName, 
        n.IPAddress,
        n.Status AS NodeStatus,
        n.IPAddress AS PollingIPAddress,
        n.MachineType,
        n.SysName AS SystemName,
        n.Description,
        n.Location,
        n.Contact,
        n.LastBoot,
        n.IOSImage,
        cp.Country,
        cp.State,
        cp.Department
    FROM 
        Orion.Nodes n
    LEFT JOIN 
        Orion.NodesCustomProperties cp ON n.NodeID = cp.NodeID
    WHERE 
        cp.DeviceType LIKE '%Switch%'
    ORDER BY 
        n.Caption
    """
    results = swis.query(query)
    return results['results']

# Example usage
devices = get_switches_with_location()

for device in devices:
    node_id = device.get('NodeID')
    device_name = device.get('DeviceName')
    ip_address = device.get('IPAddress')
    node_status = device.get('NodeStatus')
    polling_ip_address = device.get('PollingIPAddress')
    machine_type = device.get('MachineType')
    system_name = device.get('SystemName')
    description = device.get('Description', 'N/A')
    location = device.get('Location', 'N/A')
    contact = device.get('Contact', 'N/A')
    last_boot = device.get('LastBoot', 'N/A')
    ios_image = device.get('IOSImage', 'N/A')
    country = device.get('Country', 'N/A')
    state = device.get('State', 'N/A')
    department = device.get('Department', 'N/A')

    print(
        f"Node ID: {node_id}, Device Name: {device_name}, IP Address: {ip_address}, Node Status: {node_status}, "
        f"Polling IP Address: {polling_ip_address}, Machine Type: {machine_type}, System Name: {system_name}, "
        f"Description: {description}, Location: {location}, Contact: {contact}, Last Boot: {last_boot}, "
        f"IOS Image: {ios_image}, Country: {country}, State: {state}, Department: {department}"
    )
