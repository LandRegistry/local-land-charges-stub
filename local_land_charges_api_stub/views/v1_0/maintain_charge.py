import datetime
from flask import request, Blueprint, current_app
from flask_negotiate import consumes, produces
from local_land_charges_api_stub.constants.responses import AddResponses
from local_land_charges_api_stub.exceptions import ApplicationError
from local_land_charges_api_stub.utilities import add_vary_handler
from local_land_charges_api_stub.utilities.charge_id import is_valid_charge_id
from local_land_charges_api_stub.validation import validation

import json

maintain = Blueprint('maintain', __name__)


@maintain.route("", methods=["POST"])
@consumes("application/json")
@produces('application/json')
def add_charge():
    current_app.logger.info("Endpoint called")

    payload = request.get_json()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    errors = add_vary_handler.add_vary_validate(payload)

    if errors:
        error_message = {
            "error": "Charge is invalid",
            "details": errors
        }
        current_app.logger.error("Errors found: {}".format(error_message))
        raise ApplicationError(error_message, 'E100', 400)

    # checks if supplementary-information is DUPLICATE, if so raise an error
    if validation.validate_check_if_duplicate(payload):
        return (json.dumps({"duplicate_charges": ["LLC-D"]}), 409,
                {'Content-Type': 'application/json'})

    result = AddResponses.add_valid_response
    status_code = 201

    result["registration-date"] = date

    return (json.dumps(result, sort_keys=True, separators=(',', ':')), status_code,
            {'Content-Type': 'application/json'})


@maintain.route("/<land_charge_id>/<version_id>", methods=["PUT"])
@consumes("application/json")
@produces('application/json')
def vary_charge(land_charge_id, version_id):
    current_app.logger.info("Endpoint called")
    payload = request.get_json()

    if not is_valid_charge_id(land_charge_id):
        raise ApplicationError("Invalid Land Charge ID", 'E422', 422)

    if not version_id.isdigit():
        raise ApplicationError("Invalid Version ID", 'E422', 422)

    errors = add_vary_handler.add_vary_validate(payload)

    if errors:
        error_message = {
            "error": "Charge is invalid",
            "details": errors
        }
        current_app.logger.error("Errors found: {}".format(error_message))
        raise ApplicationError(error_message, 'E100', 400)

    current_app.logger.info("version_id is {}".format(version_id))
    status_code, result = AddResponses.add_vary_cancel_response(land_charge_id, version_id)

    return (json.dumps(result, sort_keys=True, separators=(',', ':')), status_code,
            {'Content-Type': 'application/json'})


@maintain.route("/<land_charge_id>/<version_id>", methods=["DELETE"])
@produces('application/json')
def cancel_charge(land_charge_id, version_id):
    current_app.logger.info("Endpoint called")

    if not is_valid_charge_id(land_charge_id):
        raise ApplicationError("Invalid Land Charge ID", 'E422', 422)

    if not version_id.isdigit():
        raise ApplicationError("Invalid Version ID", 'E422', 422)

    status_code, result = AddResponses.add_vary_cancel_response(land_charge_id, version_id)

    return (json.dumps(result, sort_keys=True, separators=(',', ':')), status_code,
            {'Content-Type': 'application/json'})
