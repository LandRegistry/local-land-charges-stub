from local_land_charges_api_stub.schema.v5_0.semantics import geometry_extent_count, validate_geometry
from local_land_charges_api_stub.schema.v6_0.semantics import validate_geometry_ids


def check_cancellation_reason(item):
    if item.get("cancellation-reason") and not item.get("end-date"):
        return [
            {
                "error_message": "'cancellation-reason' set without 'end-date'",
                "location": "$.cancellation-reason",
            }
        ]
    return []

validation_rules = [
    geometry_extent_count,
    validate_geometry,
    validate_geometry_ids,
    check_cancellation_reason,
]
