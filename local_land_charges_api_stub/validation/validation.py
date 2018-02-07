from local_land_charges_api_stub.app import app
from jsonschema import Draft4Validator, FormatChecker
from local_land_charges_api_stub.extensions import schema_extension
import json


def _format_path(error_path):
    path = '$'
    while len(error_path) > 0:
        item = error_path.popleft()
        if isinstance(item, int):
            path = "{}[{}]".format(path, item)
        else:
            path = "{}.{}".format(path, item)
    if path == '$':
        path = '$.'
    return path


def _filter_errors(messages, discard_subschemas):
    return_errors = []
    all_errors = []
    for subschema in messages:
        all_errors += messages[subschema]
        if subschema not in discard_subschemas:
            return_errors += messages[subschema]

    # Just in case - never filter out all of the messages
    if len(return_errors) == 0 and len(all_errors) > 0:
        return all_errors
    return return_errors


def _check_for_errors(data, schema, resolver):
    # Because the schema contains a number of subschemas, we'll discard error messages from
    # subschemas where it generates an error such as ' FOO is not one of [BAZ, BAR] or
    # 'FOO is not allowed for BAZ'
    validator = Draft4Validator(schema, format_checker=FormatChecker(), resolver=resolver)
    messages = {}
    discard_subschemas = []

    for error in validator.iter_errors(data):
        for suberror in error.context:
            path = _format_path(suberror.path)
            subschema = str(suberror.schema_path[0])
            if subschema not in messages:
                messages[subschema] = []

            messages[subschema].append({
                "error_message": suberror.message,
                "location": path
            })

            for subsuberror in suberror.context:
                messages[subschema].append({
                    "error_message": subsuberror.message,
                    "location": _format_path(subsuberror.path)
                })

            if path == "$.charge-type" and subschema != '0':  # Assumes all schemas will have a similar structure
                if ' is not one of ' in suberror.message or ' is not allowed for ' in suberror.message:
                    discard_subschemas.append(subschema)

    return _filter_errors(messages, discard_subschemas)


def get_item_errors(payload):
    data = payload['item']

    if 'schema-version' not in data:
        return [{
            "error_message": "'schema-version' is a required field",
            "location": "$."
        }]

    version = "v{}".format(data['schema-version'].replace('.', '_'))
    if version not in schema_extension.schema:
        return [{
            "error_message": "Unknown schema version {}".format(version),
            "location": "$.schema-version"
        }]

    app.logger.info("Validating against full schema " + json.dumps(data))
    errors = _check_for_errors(payload, schema_extension.schema[version],
                               schema_extension.resolver[version])

    # Dynamically load module for semantic validation
    for rule in schema_extension.semantic_validators[version]:
        rule_errors = rule(data)

        for re in rule_errors:
            errors.append(re)
    return errors
