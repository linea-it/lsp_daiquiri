# A list of strings representing the host/domain names that this Django site can serve.
ALLOWED_HOSTS = [
    "userquery.linea.org.br",
    "userquery-dev.linea.org.br",
    "scienceserver-dev.linea.org.br",
    "scienceserver.linea.org.br",
]

TARGET_VIEWER_URL = "https://scienceserver.linea.org.br/target/"
SCIENCE_SERVER_URL = "https://scienceserver.linea.org.br/"

QUERY_QUEUES = [
    {
        "key": "default",
        "label": "30 Seconds",
        "timeout": 30,
        "priority": 1,
        "access_level": "PUBLIC",
        "groups": [],
    },
    {
        "key": "five_minutes",
        "label": "5 Minutes",
        "timeout": 300,
        "priority": 2,
        "access_level": "PUBLIC",
        "groups": [],
    },
    {
        "key": "two_hours",
        "label": "Two hours",
        "timeout": 7200,
        "priority": 3,
        "access_level": "PUBLIC",
        "groups": [],
    },
]

# daiquiri.query.settings
# Designates if the query interface can be accessed by anonymus users.
# The permissions on schemas and tables need to be configured using the metadata interface.
# Default: False
QUERY_ANONYMOUS = True

# daiquiri.query.settings
# Sets the maximum quota for tables in a user’s personal schema.
# The quota need to be set for the anonymous user as well as regular loggen in users (user).
# Additionally, users or groups can be asigned individual quotas, e.g.:
QUERY_QUOTA = {
    "anonymous": "1Gb",
    "user": "10000Mb",
    "users": {"admin": "1000Gb"},
    "groups": {"collab": "100Gb"},
}

# daiquiri.query.settings
# Sets the timeout for syncronous (TAP) queries in seconds.
# Default: 5
QUERY_SYNC_TIMEOUT = 300
