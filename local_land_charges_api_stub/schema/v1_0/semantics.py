from local_land_charges_api_stub.app import app

MAX_NO_OF_EXTENTS = 500

s52_extra_fields = [
    'land-capacity-description',
    'land-compensation-paid'
]

s8_extra_fields = [
    'land-works-particulars',
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


def s52_required_fields(item):
    app.logger.info("Run s52 charge semantic checks")
    errors = []
    is_s52 = 'charge-type' in item and item['charge-type'] == 's52 Land Compensation Charge'
    for field in s52_extra_fields:
        if is_s52:
            if field not in item:
                errors.append({"error_message": "'{}' is a required field".format(field), "location": "$."})
        else:
            if field in item:
                errors.append({"error_message": "'{}' is an invalid field".format(field), "location": "$."})
    return errors


def s8_required_fields(item):
    app.logger.info("Run s8 charge semantic checks")
    errors = []
    is_s8 = 'charge-type' in item and item['charge-type'] == 's8 Land Compensation Charge'
    for field in s8_extra_fields:
        if is_s8:
            if field not in item:
                errors.append({"error_message": "'{}' is a required field".format(field), "location": "$."})
        else:
            if field in item:
                errors.append({"error_message": "'{}' is an invalid field".format(field), "location": "$."})
    return errors


def financial_charge_required_fields(item):
    app.logger.info("Run financial charge semantic checks")
    errors = []
    is_financial = 'charge-type' in item and item['charge-type'] in ['Specific Financial Charge']
    for field in financial_extra_fields:
        if is_financial:
            if field not in item:
                errors.append({"error_message": "'{}' is a required field".format(field), "location": "$."})
        else:
            if field in item:
                errors.append({"error_message": "'{}' is an invalid field".format(field), "location": "$."})
    return errors


def lon_charge_required_fields(item):
    app.logger.info("Run lon charge semantic checks")
    definitive_cert = 'tribunal-definitive-certificate-date'
    temporary_cert = 'tribunal-temporary-certificate-date'
    temporary_cert_expiry = 'tribunal-temporary-certificate-expiry-date'
    errors = []
    is_lon = 'charge-type' in item and item['charge-type'] in ['Light Obstruction Notice']
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


def only_one_expiry_field(item):
    app.logger.info("Run expiry field semantic checks")
    errors = []
    if 'expiry-date' in item and 'expiry-text' in item:
        errors.append({"error_message": "Must not have both 'expiry-date' and 'expiry-text'", "location": "$."})
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
    s52_required_fields,
    s8_required_fields,
    financial_charge_required_fields,
    statutory_provision_or_instrument,
    migrated_charge_fields,
    only_one_expiry_field,
    lon_charge_required_fields,
    geometry_extent_count,
    lon_servient_land_field,
    only_one_address
]
