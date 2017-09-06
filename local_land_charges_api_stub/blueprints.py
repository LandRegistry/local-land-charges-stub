# Import every blueprint file
from local_land_charges_api_stub.views import general
from local_land_charges_api_stub.views.v1_0 import maintain_charge as maintain_charge_v1_0
from local_land_charges_api_stub.views.v1_0 import retrieve_charge as retrieve_charge_v1_0


def register_blueprints(app):
    """Adds all blueprint objects into the app."""
    app.register_blueprint(general.general)
    app.register_blueprint(maintain_charge_v1_0.maintain, url_prefix='/v1.0/local-land-charges')
    app.register_blueprint(retrieve_charge_v1_0.retrieve, url_prefix='/v1.0/local-land-charges')

    # All done!
    app.logger.info("Blueprints registered")
