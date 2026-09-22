import json
import os
import sys
import pkgutil
from datetime import date, datetime
from importlib import import_module

import fastjsonschema
from jsonschema import Draft4Validator, FormatChecker

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

import schema as schema_folder

class SchemaExtension(object):
    def __init__(self, app=None):
        self.geojson_schema = {}
        self.schema = {}
        self.semantic_validators = {}

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        path = os.path.split(os.path.realpath(__file__))
        app_dir = os.path.split(path[0])[0]
        pkgpath = os.path.dirname(schema_folder.__file__)
        out_dated_pkgs = ["v1_0", "v2_0", "v3_0", "v4_0"]
        for version in [name for _, name, _ in pkgutil.iter_modules([pkgpath]) if name not in out_dated_pkgs ]:
            schema_path = os.path.join(
                app_dir, app.config["SCHEMA_RELATIVE_DIRECTORY"], version
            )
            with open(
                os.path.join(schema_path, app.config["SCHEMA_FILENAME"])
            ) as schema_file:
                schema = json.load(schema_file)
                format_checker = FormatChecker()
                self.schema[version] = Draft4Validator(
                    schema, format_checker=format_checker
                )
                register_format_checks(format_checker)

            with open(
                os.path.join(schema_path, app.config["GEOJSON_SCHEMA_FILENAME"])
            ) as schema_file:
                schema = json.load(schema_file)
                self.geojson_schema[version] = fastjsonschema.compile(schema)

            sem_mod = import_module("schema." + version + ".semantics")
            self.semantic_validators[version] = sem_mod.validation_rules


def register_format_checks(format_checker):
    @format_checker.checks("date")
    def check_date(instance):
        return validate_date(instance, True)

    @format_checker.checks("past-date")
    def check_past_date(instance):
        return validate_date(instance, False)

    @format_checker.checks("charge-creation-date")
    def check_future_date(instance):
        return validate_date(instance, False, date(1189, 7, 6))


def validate_date(instance, future, min_date=None):
    if not min_date:
        min_date = date(1925, 4, 1)
    try:
        ins_date = datetime.strptime(instance, "%Y-%m-%d").date()
        if ins_date < min_date:
            return False
        today_date = date.today()
        if not future and ins_date > today_date:
            return False
    except Exception:
        return False
    return True
