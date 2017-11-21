import os
import json
from jsonschema import RefResolver
from importlib import import_module

SCHEMA_RELATIVE_DIRECTORY = "schema"
SIMPLE_SCHEMA_FILENAME = "charge-simple.json"
INHERITED_SCHEMA_FILENAME = "charge-inherited.json"
SCHEMA_VERSIONS = ["v1_0"]


class SchemaExtension(object):

    def __init__(self, app=None):
        self.simple_resolver = {}
        self.inherited_resolver = {}
        self.simple_schema = {}
        self.inherited_schema = {}
        self.semantic_validators = {}

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        path = os.path.split(os.path.realpath(__file__))
        app_dir = os.path.split(path[0])[0]
        for version in SCHEMA_VERSIONS:
            schema_path = os.path.join(app_dir, SCHEMA_RELATIVE_DIRECTORY, version)
            with open(os.path.join(schema_path, SIMPLE_SCHEMA_FILENAME)) as simple:
                self.simple_schema[version] = json.load(simple)

            with open(os.path.join(schema_path, INHERITED_SCHEMA_FILENAME)) as inherited:
                self.inherited_schema[version] = json.load(inherited)

            self.simple_resolver[version] = RefResolver('file://' + schema_path + '/', self.simple_schema[version])
            self.inherited_resolver[version] = RefResolver(
                'file://' + schema_path + '/', self.inherited_schema[version])

            sem_mod = import_module('local_land_charges_api_stub.schema.' + version + '.semantics')
            self.semantic_validators[version] = sem_mod.validation_rules
