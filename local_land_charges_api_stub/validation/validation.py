from local_land_charges_api_stub.app import app
from local_land_charges_api_stub.validation.semantics import validation_rules
from jsonschema import Draft4Validator, FormatChecker
from local_land_charges_api_stub.extensions import schema_extension


def _check_for_errors(data, schema, resolver):
    validator = Draft4Validator(schema, format_checker=FormatChecker(), resolver=resolver)
    errors = []
    for error in validator.iter_errors(data):
        path = "$"
        while len(error.path) > 0:
            item = error.path.popleft()
            if isinstance(item, int):  # This is an assumption!
                path += "[" + str(item) + "]"
            else:
                path += "." + item
        if path == '$':
            path = '$.'

        app.logger.warning("Error at %s Message: %s", str(path), str(error.message))
        errors.append({
            "error_message": error.message,
            "location": path
        })

    return errors


def get_item_errors(data):
    app.logger.info("Validating against full schema")
    errors = _check_for_errors(data, schema_extension.simple_schema, schema_extension.simple_resolver)

    for rule in validation_rules:
        rule_errors = rule(data)

        for re in rule_errors:
            errors.append(re)
    return errors
