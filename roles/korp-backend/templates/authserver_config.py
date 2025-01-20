# -*- coding: utf-8 -*-
"""

"""
# For log levels
import logging

LOG_USING_NATIVE_PYTHON = False
LOG_USING_SYSLOG = True

# Host and port for the WSGI server
WSGI_HOST = "0.0.0.0"
WSGI_PORT = 1235

# Database host and port
DBHOST = "{{ korp_db_server }}"
DBPORT = {{korp_db_port}}
# Database name
DBNAME = "korp_auth"
# Username and password for database access
DBUSER = "{{ korp_db_user }}"
DBPASSWORD = "{{ korp_db_password }}"

# Log file and level
LOG_FILE = "/data1/korp/log/korp-auth-py.log"
LOG_LEVEL = logging.INFO  # in non-logging version, WARNING
