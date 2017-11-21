from local_land_charges_api_stub.app import app
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


def get_item_errors(data, version):
    app.logger.info("Validating against full schema")
    errors = []
    error_check = _check_for_errors(data, schema_extension.inherited_schema[version],
                                    schema_extension.inherited_resolver[version])

    if error_check:
        app.logger.warning("Errors found - checking simplified schema")
        # Simple schema produces clearer errors for returning to calling app.
        errors = _check_for_errors(data, schema_extension.simple_schema[version],
                                   schema_extension.simple_resolver[version])
    # Dynamically load module for semantic validation
    for rule in schema_extension.semantic_validators[version]:
        rule_errors = rule(data)

        for re in rule_errors:
            errors.append(re)
    return errors
