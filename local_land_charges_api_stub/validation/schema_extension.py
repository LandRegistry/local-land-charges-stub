import os
import json
from jsonschema import RefResolver

SCHEMA_RELATIVE_DIRECTORY = "schema"
SIMPLE_SCHEMA_FILENAME = "charge-simple.json"
INHERITED_SCHEMA_FILENAME = "charge-inherited.json"


class SchemaExtension(object):
    def __init__(self, app=None):
        self.simple_resolver = None
        self.inherited_resolver = None
        self.simple_schema = ''
        self.inherited_schema = ''

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        path = os.path.split(os.path.realpath(__file__))
        app_dir = os.path.split(path[0])[0]
        schema_path = os.path.join(app_dir, SCHEMA_RELATIVE_DIRECTORY)

        with open(os.path.join(schema_path, SIMPLE_SCHEMA_FILENAME)) as simple:
            self.simple_schema = json.load(simple)

        with open(os.path.join(schema_path, INHERITED_SCHEMA_FILENAME)) as inherited:
            self.inherited_schema = json.load(inherited)

        self.simple_resolver = RefResolver('file://' + schema_path + '/', self.simple_schema)
        self.inherited_resolver = RefResolver('file://' + schema_path + '/', self.inherited_schema)
