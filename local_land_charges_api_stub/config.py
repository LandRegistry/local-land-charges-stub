import os
# RULES OF CONFIG:
# 1. No region specific code. Regions are defined by setting the OS environment variables appropriately to build up the
# desired behaviour.
# 2. No use of defaults when getting OS environment variables. They must all be set to the required values prior to the
# app starting.
# 3. This is the only file in the app where os.environ should be used.

FLASK_LOG_LEVEL = os.environ['LOG_LEVEL']
COMMIT = os.environ['COMMIT']
APP_NAME = "local-land-charges-api-stub"
MAX_HEALTH_CASCADE = 6

SCHEMA_RELATIVE_DIRECTORY = "schema"
SCHEMA_FILENAME = "local-land-charge.json"
GEOJSON_SCHEMA_FILENAME = 'feature_collection.json'
