import os
import json
from jsonschema import RefResolver
from importlib import import_module

SCHEMA_RELATIVE_DIRECTORY = "schema"
SCHEMA_FILENAME = "local-land-charge.json"
SCHEMA_VERSIONS = ["v2_0", "v3_0", "v4_0", "v5_0"]


class SchemaExtension(object):

    def __init__(self, app=None):
        self.resolver = {}
        self.schema = {}
        self.semantic_validators = {}

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        path = os.path.split(os.path.realpath(__file__))
        app_dir = os.path.split(path[0])[0]
        for version in SCHEMA_VERSIONS:
            schema_path = os.path.join(app_dir, SCHEMA_RELATIVE_DIRECTORY, version)
            with open(os.path.join(schema_path, SCHEMA_FILENAME)) as simple:
                self.schema[version] = json.load(simple)

            # Get file prefix based on OS
            if os.name == 'nt':
                file_prefix = 'file:///'
            else:
                file_prefix = 'file:'

            self.resolver[version] = RefResolver(file_prefix + schema_path + '/', self.schema[version])
            sem_mod = import_module('local_land_charges_api_stub.schema.' + version + '.semantics')
            self.semantic_validators[version] = sem_mod.validation_rules
