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
    errors = []
    category = get_charge_category(charge["charge-type"])
    if not category or charge["charge-type"] != category['name']:
        errors.append({"location": "$.item.charge-type",
                       "error_message": "'{}' is not valid".format(charge['charge-type'])})
    else:
        instruments = None
        if 'sub-categories' in category and category['sub-categories']:
            if 'charge-sub-category' in charge and charge['charge-sub-category']:
                valid_sub_cats = [sub['name'] for sub in category['sub-categories']]
                if charge['charge-sub-category'] not in valid_sub_cats:
                    errors.append({"location": "$.item.charge-sub-category",
                                   "error_message":
                                       "'{}' is not valid".format(charge['charge-sub-category'])})
                else:
                    sub_category = get_charge_sub_category(charge['charge-type'],
                                                           charge['charge-sub-category'])
                    if 'instruments' in sub_category and sub_category['instruments']:
                        instruments = sub_category['instruments']
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
            instruments = [instrument for instrument in instruments]
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
    # TODO change this to not use database but instead use a dictionary of the database values
    app.logger.info("Get category for {0}.".format(category))

    category_obj = Categories.query \
        .filter(func.lower(Categories.name) == func.lower(category)) \
        .filter(Categories.parent_id == None) \
        .first()  # noqa: E711 - Ignore "is None vs ==" linting error, is None does not produce valid sql in sqlAlchmey

    if category_obj is None:
        raise ApplicationError("Category '{0}' not found.".format(category), 404, 404)

    provisions = []
    for provision_mapping in category_obj.provisions:
        provisions.append(provision_mapping.provision.title)

    instruments = []
    for instruments_mapping in category_obj.instruments:
        instruments.append(instruments_mapping.instrument.name)

    children = []
    for children_mapping in Categories.query \
            .filter(Categories.parent_id == category_obj.id) \
            .order_by(Categories.display_order).all():
        children.append(
            {
                "name": children_mapping.name,
                "display-name": children_mapping.display_name,
                "permission": children_mapping.permission,

            })

    result = {
        "name": category_obj.name,
        "display-name": category_obj.display_name,
        "permission": category_obj.permission,
        "statutory-provisions": provisions,
        "instruments": instruments,
        "sub-categories": children}

    return result


def get_charge_sub_category(category, sub_category):
    # TODO change this to not use database but instead use a dictionary of the database values
    app.logger.info("Get category for {0}.".format(category))

    category_obj = Categories.query \
        .filter(func.lower(Categories.name) == func.lower(category)) \
        .filter(Categories.parent_id == None) \
        .first()  # noqa: E711 - Ignore "is None vs ==", is None does not produce valid sql in sqlAlchmey

    if category_obj is None:
        raise ApplicationError("Category '{0}' not found.".format(category), 404, 404)

    sub_category_obj = Categories.query \
        .filter(func.lower(Categories.name) == func.lower(sub_category)) \
        .filter(Categories.parent_id == category_obj.id) \
        .first()

    if sub_category_obj is None:
        raise ApplicationError("Sub-category '{0}' not found for parent '{1}'".format(sub_category, category),
                               404, 404)

    provisions = []
    for provision_mapping in sub_category_obj.provisions:
        provisions.append(provision_mapping.provision.title)

    instruments = []
    for instruments_mapping in sub_category_obj.instruments:
        instruments.append(instruments_mapping.instrument.name)

    children = []
    for children_mapping in Categories.query \
            .filter(Categories.parent_id == sub_category_obj.id) \
            .order_by(Categories.display_order).all():
        children.append(
            {
                "name": children_mapping.name,
                "display-name": children_mapping.display_name,
                "permission": children_mapping.permission,

            })

    result = {
        "name": sub_category_obj.name,
        "display-name": sub_category_obj.display_name,
        "permission": sub_category_obj.permission,
        "statutory-provisions": provisions,
        "instruments": instruments,
        "sub-categories": children,
        "parent": category_obj.name}

    return result
