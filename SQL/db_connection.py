# SQL/db_connection.py

import pymysql
import logging

def connect_to_sql_server():
    try:
        connection = pymysql.connect(
            host='192.168.10.12',
            user='mgcather',     # Your MySQL username
            password='plexmaster', # Your MySQL password
            db='Networking',     # Your database name
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        logging.info("Connection to MySQL database established successfully.")
        return connection
    except Exception as e:
        logging.error(f"Failed to connect to MySQL database: {e}")
        return None
