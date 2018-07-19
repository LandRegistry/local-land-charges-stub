from local_land_charges_api_stub.app import app
from jsonschema import Draft4Validator, FormatChecker
from local_land_charges_api_stub.exceptions import ApplicationError
from local_land_charges_api_stub.extensions import schema_extension
from local_land_charges_api_stub.validation.categories import category_dict
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

    if data['schema-version'] == '5.0':
        # version 5 of the schema moved category validation from schema to code, so validate this now
        errors += validate_category_instrument(data)

    # Dynamically load module for semantic validation
    for rule in schema_extension.semantic_validators[version]:
        rule_errors = rule(data)

        for re in rule_errors:
            errors.append(re)
    return errors


def validate_category_instrument(charge):
    """
    Validate the category, sub-category (if present), and instrument (if present) against valid values in
    validation/categories.py dictionary
    :param charge: the charge object
    :return: a list of errors if any are present, an empty list if the category/sub-category/instrument are valid
    """
    errors = []
    category, error = get_charge_category(charge["charge-type"])
    if error:
        errors.append(error)
    else:
        instruments = None
        if 'sub-categories' in category and category['sub-categories']:
            if 'charge-sub-category' in charge and charge['charge-sub-category']:
                if charge['charge-sub-category'] not in category['sub-categories']:
                    errors.append({"location": "$.item.charge-sub-category",
                                   "error_message":
                                       "'{}' is not valid".format(charge['charge-sub-category'])})
                else:
                    valid_instruments, error = get_sub_category_instruments(charge['charge-type'],
                                                                            charge['charge-sub-category'])
                    if error:
                        errors.append(error)
                    elif valid_instruments:
                        instruments = valid_instruments
            else:
                errors.append({"location": "$.item",
                               "error_message":
                                   "'charge-sub-category' is required"})
        elif 'charge-sub-category' in charge and charge['charge-sub-category']:
            errors.append(
                {"location": "$.item",
                 "error_message":
                     "Additional properties are not allowed ('charge-sub-category' was unexpected)"})
        if not instruments and 'instruments' in category and category['instruments']:
            instruments = category['instruments']
        if instruments:
            if 'instrument' in charge and charge['instrument']:
                if charge['instrument'] not in instruments:
                    errors.append({"location": "$.item.instrument",
                                   "error_message":
                                       "'{}' is not valid".format(charge['instrument'])})
            else:
                errors.append({"location": "$.item", "error_message": "'instrument' is required"})
        else:
            if 'instrument' in charge and charge['instrument']:
                errors.append({"location": "$.item",
                               "error_message":
                                   "Additional properties are not allowed ('instrument' was unexpected)"})
    return errors


def get_charge_category(category):
    """
    Check that a charge category exists in the validation/categories.py dictionary, and return the details if so
    :param category: The name of the category to check
    :return: dict of instruments and sub-categories if category valid, empty dict if invalid
             empty dict if category valid, dict of error if invalid
    """
    app.logger.info("Get category for {0}.".format(category))

    if category in category_dict:
        category_obj = category_dict[category]
    else:
        return {}, {"location": "$.item.charge-type", "error_message": "'{}' is not valid".format(category)}

    instruments = []
    if "instruments" in category_obj:
        instruments = category_obj["instruments"]

    children = []
    if "sub-categories" in category_obj:
        children = list(category_obj["sub-categories"].keys())

    result = {
        "instruments": instruments,
        "sub-categories": children
    }

    return result, {}


def get_sub_category_instruments(category, sub_category):
    """
    Check that a charge category exists and has a sub-category, in the validation/categories.py dictionary, and
    returns the instruments for the sub-category if any exist
    :param category: The name of the category to check
    :param sub_category: The name of the sub-category to check
    :return: list of instruments if any exist, or empty list if none exist or any errors are present
             empty dict if no errors, dict of error details if errors are present
    """
    app.logger.info("Get sub-category {1} for category {0}.".format(category, sub_category))

    if category in category_dict:
        category_obj = category_dict[category]
    else:
        return [], {"location": "$.item.charge-type", "error_message": "'{}' is not valid".format(category)}

    if "sub-categories" in category_obj and sub_category in category_obj["sub-categories"]:
        sub_category_obj = category_obj["sub-categories"][sub_category]
    else:
        return [], {"location": "$.item.charge-sub-category", "error_message": "'{}' is not valid".format(sub_category)}

    instruments = []
    if "instruments" in sub_category_obj:
        instruments = sub_category_obj["instruments"]

    return instruments, {}
