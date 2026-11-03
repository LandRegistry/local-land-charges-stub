from local_land_charges_api_stub.schema.v5_0.semantics import geometry_extent_count, validate_geometry
from local_land_charges_api_stub.app import app


def validate_geometry_ids(item):
    errors = []
    app.logger.info("Run geometry id validation checks")
    if 'geometry' in item and 'features' in item['geometry']:
        collection_ids = []
        for idx, feature in enumerate(item['geometry']['features']):
            if 'properties' in feature and 'id' in feature['properties']:
                feature_id = feature['properties']['id']
                if feature_id in collection_ids:
                    errors.append({"location": "$.geometry.features[{}].properties.id".format(idx),
                                   "error_message": "Duplicate Feature ID '{}'".format(feature_id)})
                else:
                    collection_ids.append(feature_id)

    return errors

validation_rules = [
    geometry_extent_count,
    validate_geometry_ids,
    validate_geometry
]
