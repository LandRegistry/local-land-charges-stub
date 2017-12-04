import re
from local_land_charges_api_stub.app import app

MAX_NO_OF_EXTENTS = 500

s52_extra_fields = [
    'land-capacity-description',
    'land-compensation-paid',
    'land-compensation-amount-type'
]

s8_extra_fields = [
    'land-sold-description',
    'land-works-particulars'
]

financial_extra_fields = [
    'amount-originally-secured',
    'rate-of-interest'
]

migration_required_fields = [
    'old-register-part',
    'migrating-authority',
    'migration-supplier'
]

lon_required_fields = [
    'applicant-name',
    'applicant-address',
    'servient-land-interest-description',
    'structure-position-and-dimension',
    'documents-filed'
]


def lca_charge_required_fields(item):
    app.logger.info("Run Land Compensation Act semantic checks")
    errors = []
    is_lca = 'charge-type' in item and item['charge-type'] == 'Land compensation'
    if is_lca:
        is_s8 = 'land-sold-description' in item and 'land-works-particulars' in item
        is_s52 = 'land-capacity-description' in item and 'land-compensation-paid' in item \
            and 'land-compensation-amount-type' in item
        if not (is_s8 or is_s52) or (is_s8 and is_s52):
            errors.append({"error_message": "Only 'land-sold-description' with 'land-works-particulars' or " +
                           "'land-capacity-description' with 'land-compensation-paid' and " +
                           "'land-compensation-amount-type' combinations are acceptable", "location": "$."})
        else:
            if is_s52:
                amount_pattern = r'^\d+(?:\.\d{2})?$'
                if not re.match(amount_pattern, item['land-compensation-paid']):
                    errors.append({"error_message": "'land-compensation-paid' must be a number " +
                                   "(either an integer or with 2 decimal places)", "location": "$."})
                for field in s8_extra_fields:
                    if field in item:
                        errors.append({"error_message": "'{}' is an invalid field".format(field), "location": "$."})
            else:  # is_s8
                for field in s52_extra_fields:
                    if field in item:
                        errors.append({"error_message": "'{}' is an invalid field".format(field), "location": "$."})
    else:
        for field in s52_extra_fields:
            if field in item:
                errors.append({"error_message": "'{}' is an invalid field".format(field), "location": "$."})

        for field in s8_extra_fields:
            if field in item:
                errors.append({"error_message": "'{}' is an invalid field".format(field), "location": "$."})
    return errors


def financial_charge_required_fields(item):
    app.logger.info("Run financial charge semantic checks")
    errors = []
    is_financial = 'charge-type' in item and item['charge-type'] == 'Financial'
    has_amount = 'amount-originally-secured' in item
    amount_pattern = r'^\d+(?:\.\d{2})?$'
    rate_pattern = r'^\d+(?:\.\d{1,2})?$'
    if is_financial:
        if has_amount and not re.match(amount_pattern, item['amount-originally-secured']):
            errors.append({"error_message": "'amount-originally-secured' must be a number " +
                           "(either an integer or with 2 decimal places)", "location": "$."})
        if 'rate-of-interest' in item:
            if not has_amount:
                errors.append({"error_message": "'rate-of-interest' cannot be supplied if " +
                               "'amount-originally-secured' is not present", "location": "$."})
            if (not re.match(rate_pattern, item['rate-of-interest']) and
                    not item['rate-of-interest'] == 'Interest may be payable'):
                errors.append({"error_message": "'rate-of-interest' must be either a number " +
                               "(up to 2 decimal places) or 'Interest may be payable'", "location": "$."})
    else:
        for field in financial_extra_fields:
            if field in item:
                errors.append({"error_message": "'{}' is an invalid field".format(field), "location": "$."})
    return errors


def lon_charge_required_fields(item):
    app.logger.info("Run lon charge semantic checks")
    definitive_cert = 'tribunal-definitive-certificate-date'
    temporary_cert = 'tribunal-temporary-certificate-date'
    temporary_cert_expiry = 'tribunal-temporary-certificate-expiry-date'
    errors = []
    is_lon = 'charge-type' in item and item['charge-type'] in ['Light obstruction notice']
    if is_lon:
        if definitive_cert not in item and temporary_cert not in item:
            errors.append({"error_message": "At least one of '{}' or '{}' is required".format(
                definitive_cert, temporary_cert), "location": "$."})
        elif temporary_cert in item and temporary_cert_expiry not in item:
            errors.append({"error_message": "'{}' is required if '{}' is present".format(
                temporary_cert_expiry, temporary_cert), "location": "$."})
        elif temporary_cert_expiry in item and temporary_cert not in item:
            errors.append({"error_message": "'{}' cannot be supplied if '{}' is not present".format(
                temporary_cert_expiry, temporary_cert), "location": "$."})
        for field in lon_required_fields:
            if field not in item:
                errors.append({"error_message": "'{}' is a required field".format(field), "location": "$."})
    else:
        for field in lon_required_fields:
            if field in item:
                errors.append({"error_message": "'{}' is an invalid field".format(field), "location": "$."})
            elif definitive_cert in item:
                errors.append({"error_message": "'{}' is an invalid field".format(definitive_cert), "location": "$."})
            elif temporary_cert in item:
                errors.append({"error_message": "'{}' is an invalid field".format(temporary_cert), "location": "$."})
            elif temporary_cert_expiry in item:
                errors.append({"error_message": "'{}' is an invalid field".format(
                    temporary_cert_expiry), "location": "$."})
    return errors


def statutory_provision_or_instrument(item):
    app.logger.info("Run provision/instrument semantic checks")
    errors = []
    if 'statutory-provision' not in item and 'instrument' not in item:
        errors.append({"error_message": "Either 'statutory-provision' or 'instrument' is required", "location": "$."})
    return errors


def migrated_charge_fields(item):
    # TODO(unknown): test the assumption about migrating-authority
    app.logger.info("Run migrated charge semantic checks")
    errors = []
    is_migrated = 'migrating-authority' in item
    for field in migration_required_fields:
        if is_migrated:
            if field not in item:
                errors.append({"error_message": "'{}' is a required field".format(field), "location": "$."})
        else:
            if field in item:
                errors.append({"error_message": "'{}' is an invalid field".format(field), "location": "$."})
    return errors


def geometry_extent_count(item):
    app.logger.info("Run geometry extent count semantic checks")
    errors = []
    if 'geometry' in item and 'features' in item['geometry']:
        extents = item['geometry']['features']
        if len(extents) > int(MAX_NO_OF_EXTENTS):
            errors.append({"error_message": "Number of extents exceeds permitted maximum of {}".format(
                MAX_NO_OF_EXTENTS), "location": "$.geometry.features"})
    return errors


def lon_servient_land_field(item):
    errors = []
    is_lon = 'charge-type' in item and item['charge-type'] in ['Light Obstruction Notice']
    if is_lon:
        servient_land = item['structure-position-and-dimension']
        if servient_land['height'] != 'Unlimited height' and 'units' not in servient_land:
            errors.append({'error_message': 'Units required for limited height',
                           'location': '$.structure-position-and-dimension'})

        if servient_land['height'] == 'Unlimited height' and 'units' in servient_land:
            errors.append({'error_message': 'Units must not be supplied for limited height',
                           'location': '$.structure-position-and-dimension'})

        if servient_land['extent-covered'] == "All of the extent" and 'part-explanatory-text' in servient_land:
            errors.append({'error_message': 'part-explanatory-text is not permitted when extent-covered '
                                            'is "All of the extent"',
                           'location': '$.structure-position-and-dimension'})

        if servient_land['extent-covered'] == "Part of the extent" \
                and 'part-explanatory-text' not in servient_land:
            errors.append({'error_message': 'part-explanatory-text is required when extent-covered is'
                                            ' "Part of the extent"',
                           'location': '$.structure-position-and-dimension'})
    return errors


def only_one_address(item):
    geo = 'charge-geographic-description' in item
    address = 'charge-address' in item
    errors = []
    if geo and address:
        errors.append({'error_message': 'Must not have both charge-geographic-description and charge-address',
                       'location': '$.'})

    if not geo and not address:
        errors.append({'error_message': 'Must have one of charge-geographic-description or charge-address',
                       'location': '$.'})

    return errors


validation_rules = [
    lca_charge_required_fields,
    financial_charge_required_fields,
    statutory_provision_or_instrument,
    migrated_charge_fields,
    lon_charge_required_fields,
    geometry_extent_count,
    lon_servient_land_field,
    only_one_address
]
