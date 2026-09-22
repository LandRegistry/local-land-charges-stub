import json

import geojson
from shapely.errors import GeometryTypeError
from shapely.geometry import shape
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


def validate_geometry(item):
    errors = []

    if item.get('geometry') and item['geometry'].get('features'):
        try:
            parsed_geojson = geojson.loads(json.dumps(item['geometry']))
            if not isinstance(parsed_geojson, geojson.FeatureCollection) or not parsed_geojson.is_valid:
                raise Exception("Error handling geojson")
        except Exception:
            errors.append({"location": "$.geometry",
                           "error_message": "geojson is not valid"})
        for idx, feature in enumerate(item['geometry']['features']):
            try:
                geo_shape = shape(feature['geometry'])
                if not geo_shape.is_simple:
                    new_geom = geo_shape.simplify(0)
                    is_simple = new_geom.is_simple
                    if not is_simple:
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
            except shapely.errors.PredicateError:
                errors.append({"location": "$.geometry.features[{}].geometry".format(idx),
                               "error_message": "Shapely Predicate error, check interior rings"})
            except ValueError:
                errors.append({"location": "$.geometry.features[{}].geometry".format(idx),
                               "error_message": "Geometry is invalid"})
            except Exception:
                errors.append({"location": "$.geometry.features[{}].geometry".format(idx),
                                "error_message": "Geometry is invalid"})

    return errors


validation_rules = [
    geometry_extent_count,
    validate_geometry
]