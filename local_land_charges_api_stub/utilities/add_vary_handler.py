from local_land_charges_api_stub.constants.constants import AddChargeConstants
from local_land_charges_api_stub.validation import validation


def add_vary_validate(payload):
    errors = []
    if 'item' not in payload:
        errors.append({"location": "$.", "error_message": "'item' is a required property"})
    else:
        charge_data = payload['item']
        if 'local-land-charge' in charge_data:
            errors.append({"location": "$.item", "error_message":
                           "Additional properties are not allowed ('local-land-charge' was unexpected)"})

        if 'start-date' in charge_data:
            errors.append({"location": "$.item", "error_message":
                           "Additional properties are not allowed ('start-date' was unexpected)"})

        # Prevent Author being set as we set this before submission
        if 'author' in charge_data:
            errors.append({"location": "$.item",
                           "error_message": "Additional properties are not allowed ('author' was unexpected)"})

        if 'statutory-provision' in charge_data:
            stat_prov_list = AddChargeConstants.STATUTORY_PROVISION
            if charge_data['statutory-provision'] not in stat_prov_list:
                errors.append({"location": "$.item.statutory-provision",
                               "error_message": "'{}' is not valid".format(charge_data['statutory-provision'])})

        # Prevent LONs
        if 'charge-type' in charge_data:
            if charge_data['charge-type'] in ['Light Obstruction Notice']:
                errors.append({"location": "$.item.charge-type",
                               "error_message": "'{}' is not valid".format(charge_data['charge-type'])})

        schema_errors = validation.get_item_errors(charge_data)
        if schema_errors:
            errors.extend(schema_errors)

    return errors
