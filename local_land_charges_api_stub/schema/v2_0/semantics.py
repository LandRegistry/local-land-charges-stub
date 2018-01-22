from validation_api.app import app
from validation_api.config import MAX_NO_OF_EXTENTS
from shapely.geometry import shape


def geometry_extent_count(item):
    app.logger.info("Run geometry extent count semantic checks")
    errors = []
    if 'geometry' in item and 'features' in item['geometry']:
        extents = item['geometry']['features']
        if len(extents) > int(MAX_NO_OF_EXTENTS):
            errors.append({"error_message": "Number of extents exceeds permitted maximum of {}".format(
                MAX_NO_OF_EXTENTS), "location": "$.geometry.features"})
    return errors


def validate_geometry(item):
    errors = []
    app.logger.info("Run geometry validation checks")
    if 'geometry' in item and 'features' in item['geometry']:
        for idx, feature in enumerate(item['geometry']['features']):
            geo_shape = shape(feature['geometry'])
            if not geo_shape.is_simple:
                errors.append({"location": "$.geometry.features[{}].geometry".format(idx),
                               "error_message": "geometry must be simple"})
            if not geo_shape.is_valid:
                errors.append({"location": "$.geometry.features[{}].geometry".format(idx),
                               "error_message": "geometry must be simple and valid"})
            if feature['geometry']['type'] == 'LineString' and geo_shape.length == 0.0:
                errors.append({"location": "$.geometry.features[{}].geometry".format(idx),
                               "error_message": "LineStrings must not be zero length"})
            if feature['geometry']['type'] == 'Polygon' and geo_shape.area == 0.0:
                errors.append({"location": "$.geometry.features[{}].geometry".format(idx),
                               "error_message": "Polygon must not be zero area"})
    return errors


validation_rules = [
    geometry_extent_count,
    validate_geometry
]
