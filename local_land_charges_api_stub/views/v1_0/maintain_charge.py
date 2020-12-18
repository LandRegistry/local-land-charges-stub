import datetime
from flask import request, Blueprint, current_app
from flask_negotiate import consumes, produces
from local_land_charges_api_stub.constants.responses import AddResponses
from local_land_charges_api_stub.exceptions import ApplicationError
from local_land_charges_api_stub.utilities import add_vary_handler
from local_land_charges_api_stub.utilities.charge_id import is_valid_charge_id

import json

maintain = Blueprint('maintain', __name__)


@maintain.route("", methods=["POST"])
# doesn't work with this
# @consumes("application/json")
# @produces('application/json')
def add_charge():
    current_app.logger.info("Endpoint called")
    payload = request.get_json()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    print(payload)
    errors = add_vary_handler.add_vary_validate(payload)

    if errors:
        error_message = {
            "error": "Charge is invalid",
            "details": errors
        }
        current_app.logger.error("Errors found: {}".format(error_message))
        raise ApplicationError(error_message, 'E100', 400)

    result = AddResponses.add_valid_response
    status_code = 200

    result["registration-date"] = date

    current_app.logger.info("Charge sent to maintain-api - Building response")

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

    current_app.logger.info("Sending charge to maintain-api")
    status_code, result = AddResponses.add_vary_cancel_response(land_charge_id, version_id)

    if status_code == 400:
        current_app.logger.error("Errors found: {}".format(result[0]))
        raise ApplicationError(result[0], 'E400', status_code)

    current_app.logger.info("Charge sent to maintain-api - Building response")

    return (json.dumps(result, sort_keys=True, separators=(',', ':')), status_code,
            {'Content-Type': 'application/json'})
