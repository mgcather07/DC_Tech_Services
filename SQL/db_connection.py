import pyodbc
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def connect_to_sql_server():
    try:
        logging.info("Attempting to connect to the SQL Server database.")
        logging.debug(f"Using server: CORSQLP006")
        logging.debug(f"Using database: Network_Automation")
        logging.debug(f"Using UID: {os.environ.get('SQL_USERNAME')}")

        if 'SQL_USERNAME' not in os.environ or 'SQL_PASSWORD' not in os.environ:
            logging.error("Environment variables for SQL credentials are not set.")
            return None

        connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=CORSQLP006;'
            'DATABASE=Network_Automation;'
            f'UID={os.environ["SQL_USERNAME"]};'
            f'PWD={os.environ["SQL_PASSWORD"]}'
        )
        logging.debug(f"Connection string: {connection_string}")

        connection = pyodbc.connect(connection_string)
        logging.info("Successfully connected to the SQL Server database.")
        return connection
    except pyodbc.Error as err:
        logging.error(f"Error: {err}")
        return None