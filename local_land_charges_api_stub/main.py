# This file is the entry point.
# First we import the app object, which will get initialised as we do it. Then import methods we're about to use.
from local_land_charges_api_stub.app import app
from local_land_charges_api_stub.blueprints import register_blueprints
from local_land_charges_api_stub.extensions import register_extensions
from local_land_charges_api_stub.exceptions import register_exception_handlers

# Now we register any extensions we use into the app
register_extensions(app)
# Register the exception handlers
register_exception_handlers(app)
# Finally we register our blueprints to get our routes up and running.
register_blueprints(app)
