
"""
korpplugins.protectedcorporadb.config (template)

Sample configuration for korpplugins.protectedcorporadb.
"""

# All MySQL connection parameters as a dict; if non-empty, the values it
# contains override the individual DBCONN_* values
DBCONN_PARAMS = {}

# Database host and port
DBCONN_HOST = "{{ korp_db_server }}"
DBCONN_PORT = "{{ korp_db_port }}"
# Database name
DBCONN_DB = "korp_auth"
# Username and password for database access
DBCONN_USER = "{{ korp_db_user }}"
DBCONN_PASSWORD = "{{ korp_db_password }}"
DBCONN_USE_UNICODE = True
DBCONN_CHARSET = "utf8mb4"

# The name of the table in DBCONN_DB from which to retrieve licence
# information
LICENCE_TABLE = "auth_license"

# The SQL statement to list protected corpora in DBCONN_DB;
# {LICENCE_TABLE} is replaced with the value of LICENCE_TABLE.
LIST_PROTECTED_CORPORA_SQL = """
    SELECT corpus FROM {LICENCE_TABLE}
    WHERE NOT license LIKE 'PUB%'
"""

# Whether to keep the database connection persistent (True) or close
# after each call of filter_protected_corpora (False)
PERSISTENT_DB_CONNECTION = True
