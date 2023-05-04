# -*- coding: utf-8 -*-
"""
Configuration file used by the main korp.py script.

Copy this file to config.py and change the settings below.
"""

# Host and port for the WSGI server
WSGI_HOST = "0.0.0.0"
WSGI_PORT = 1234

# The absolute path to the CQP binaries
CQP_EXECUTABLE = "/usr/local/bin/cqp"
CWB_SCAN_EXECUTABLE = "/usr/local/bin/cwb-scan-corpus"

# The absolute path to the CWB registry files
CWB_REGISTRY = "{{ cwb_registry }}"

# The default encoding for the cqp binary
CQP_ENCODING = "UTF-8"

# Locale to use when sorting
LC_COLLATE = "sv_SE.UTF-8"

# The maximum number of search results that can be returned per query (0 = no limit)
MAX_KWIC_ROWS = 0

# Number of threads to use during parallel processing
PARALLEL_THREADS = 3

# Database host and port
DBHOST = "{{ korp_db_server }}"
DBPORT = {{ korp_db_port }}
# Database name
DBNAME = "korp"
# Username and password for database access
DBUSER = "{{ korp_db_user }}"
DBPASSWORD = "{{ korp_db_password }}"

# Database character set
DBCHARSET = "utf8mb4"

# Word Picture table prefix
DBWPTABLE = "relations"

# Database collation for lemgram data
DBCOLLATE_LEMGRAM = "utf8mb4_bin"

# URL to authentication server
AUTH_SERVER = "http://localhost:1235"

# Secret string used when communicating with authentication server
AUTH_SECRET = ""

# A text file with names of corpora needing authentication, one per line
PROTECTED_FILE = ""

# Cache path (optional). Script must have read and write access.
CACHE_DIR = "{{ backend_cache_dir }}"

# Disk cache lifespan in minutes
CACHE_LIFESPAN = 20

# List of Memcached servers or sockets (socket paths must start with slash)
MEMCACHED_SERVERS = ["localhost:11211"]

# Size of Memcached client pool
MEMCACHED_POOL_SIZE = 25

# Max number of rows from count command to cache
CACHE_MAX_STATS = 5000

# Whether corpus results should be sorted by corpus id by default (true) or
# output in the order specified in the corpus parameter (false); this can be
# overridden with the parameter sort_corpora=true|false
SORT_CORPORA_DEFAULT = True

# List of names of plugin modules to load
PLUGINS = [
    "charcoder",
    "logger",
    "lemgramcompleter",
    "contenthider",
    "protectedcorporadb",
    "shibauth",
]

# Show plugin information in the result of the /info command: "name" = plugin
# names only, "info" = plugin information in the PLUGIN_INFO of the plugin,
# None = nothing
INFO_SHOW_PLUGINS = "info"

# korppluginlib configuration: the values here override those in
# korppluginlib.config; comment these out to use the defaults. For
# more information, see korppluginlib.config.

PLUGINLIB_CONFIG = dict(
    # Packages which may contain plugins; "" for top-level modules
    PACKAGES = ["korpplugins"],
    # Directories to search for plugins (packages) in addition to default ones
    SEARCH_PATH = ["{{ korp_backend_plugin_home }}"],
    
    # What to do when a plugin is not found: "error", "warn" or "ignore"
    HANDLE_NOT_FOUND = "warn",
    # What to output when loading plugins: 0 = nothing, 1 = plugin names,
    # 2 = plugin and plugin function names
    LOAD_VERBOSITY = 1,
)
