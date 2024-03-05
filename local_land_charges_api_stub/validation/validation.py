from local_land_charges_api_stub.app import app
from jsonschema import Draft4Validator, FormatChecker
from local_land_charges_api_stub.exceptions import ApplicationError
from local_land_charges_api_stub.extensions import schema_extension
from local_land_charges_api_stub.validation.categories import Categories
from local_land_charges_api_stub.validation.instruments import instruments_list
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


def get_item_errors(data):
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
    errors = _check_for_errors(data, schema_extension.schema[version],
                               schema_extension.resolver[version])

    if data['schema-version'] >= '5.0':
        # from version 5, category validation moved out of the schema, so validate this now
        errors += validate_category_instrument(data)

    # Dynamically load module for semantic validation
    for rule in schema_extension.semantic_validators[version]:
        rule_errors = rule(data)

        for re in rule_errors:
            errors.append(re)
    return errors


def validate_check_if_duplicate(payload):
    """
    Validate the the charge to make sure it is not a duplicate
    :param charge: the charge object
    :return: a list of errors if any are present, an empty list if charge is not duplicated
    """
    if payload['item'].get('supplementary-information', '') == "DUPLICATE":
        return {"duplicate_charges": ["LLC-D"]}
    return []


def validate_category_instrument(charge):
    """
    Validate the category, sub-category (if present), and instrument (if present) against valid values in
    validation/categories.py dictionary and instruments.py
    :param charge: the charge object
    :return: a list of errors if any are present, an empty list if the category/sub-category/instrument are valid
    """
    errors = []
    category, error = get_charge_category(charge["charge-type"])
    if error:
        errors.append(error)
    else:
        if category.get('sub-categories', None):
            if charge.get('charge-sub-category', None):
                if charge['charge-sub-category'] not in category['sub-categories']:
                    errors.append({"location": "$.item.charge-sub-category",
                                   "error_message":
                                       "'{}' is not valid".format(charge['charge-sub-category'])})
            else:
                errors.append({"location": "$.item",
                               "error_message":
                                   "'charge-sub-category' is required"})
        elif 'charge-sub-category' in charge and charge['charge-sub-category']:
            errors.append(
                {"location": "$.item",
                 "error_message":
                     "Additional properties are not allowed ('charge-sub-category' was unexpected)"})

    if charge.get('instrument', None):
        if charge['instrument'] not in instruments_list:
            errors.append({"location": "$.item.instrument",
                           "error_message": "'{}' is not valid".format(charge['instrument'])})

    return errors


def get_charge_category(category):
    """
    Check that a charge category exists in the validation/categories.py dictionary, and return the details if so
    :param category: The name of the category to check
    :return: dict of sub-categories if category valid, empty dict if invalid
             empty dict if category valid, dict of error if invalid
    """
    app.logger.info("Get category for {0}.".format(category))

    category_data=Categories().get_category_data()
    if category in category_data:
        category_obj = category_data[category]
    else:
        return {}, {"location": "$.item.charge-type", "error_message": "'{}' is not valid".format(category)}

    children = []
    if "sub-categories" in category_obj:
        children = list(category_obj["sub-categories"].keys())

    result = {
        "sub-categories": children
    }

    return result, {}
