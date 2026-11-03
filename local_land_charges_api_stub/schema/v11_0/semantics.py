from local_land_charges_api_stub.schema.v5_0.semantics import geometry_extent_count, validate_geometry
from local_land_charges_api_stub.schema.v6_0.semantics import validate_geometry_ids
from local_land_charges_api_stub.schema.v9_0.semantics import check_cancellation_reason

validation_rules = [
    geometry_extent_count,
    validate_geometry,
    validate_geometry_ids,
    check_cancellation_reason,
]
