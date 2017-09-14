from local_land_charges_api_stub.custom_extensions.enhanced_logging.main import EnhancedLogging
from local_land_charges_api_stub.validation.schema_extension import SchemaExtension


# Create empty extension objects here
enhanced_logging = EnhancedLogging()
schema_extension = SchemaExtension()


def register_extensions(app):
    """Adds any previously created extension objects into the app, and does any further setup they need."""

    # This extension wraps the LogConfig extension with our own configuration (standard format JSON -> stdout
    # plus traceid parsing and propagation in a custom Requests Session)
    enhanced_logging.init_app(app)

    schema_extension.init_app(app)

    # All done!
    app.logger.info("Extensions registered")
