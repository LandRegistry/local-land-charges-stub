import os
# RULES OF CONFIG:
# 1. No region specific code. Regions are defined by setting the OS environment variables appropriately to build up the
# desired behaviour.
# 2. No use of defaults when getting OS environment variables. They must all be set to the required values prior to the
# app starting.
# 3. This is the only file in the app where os.environ should be used.

# For the enhanced logging extension
FLASK_LOG_LEVEL = os.environ['LOG_LEVEL']

# For health route
COMMIT = os.environ['COMMIT']

# This APP_NAME variable is to allow changing the app name when the app is running in a cluster. So that
# each app in the cluster will have a unique name.
APP_NAME = "local-land-charges-api-stub"
MAX_HEALTH_CASCADE = 6

# Following is an example of building the dependency structure used by the cascade route
# SELF can be used to demonstrate how it works (i.e. it will call it's own casecade
# route until MAX_HEALTH_CASCADE is hit)
# SELF = "http://localhost:8080"
# DEPENDENCIES = {"SELF": SELF}
# DEPENDENCIES = {"Maintain API": os.environ['MAINTAIN_API_ROOT']}
