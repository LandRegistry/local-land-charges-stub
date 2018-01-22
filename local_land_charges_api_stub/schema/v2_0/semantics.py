from local_land_charges_api_stub.app import app


def geometry_extent_count(item):
    app.logger.info("Run geometry extent count semantic checks")
    errors = []
    if 'geometry' in item and 'features' in item['geometry']:
        extents = item['geometry']['features']
        if len(extents) > 500:
            errors.append({"error_message": "Number of extents exceeds permitted maximum of {}".format(
                500), "location": "$.geometry.features"})
    return errors


validation_rules = [
    geometry_extent_count
]
