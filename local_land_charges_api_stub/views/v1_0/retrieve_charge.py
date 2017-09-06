from flask import Blueprint, current_app
from local_land_charges_api_stub.utilities import response_handler
import json

retrieve = Blueprint('retrieve', __name__)


@retrieve.route("/<charge_id>", methods=["GET"])
def get_charge(charge_id):
    current_app.logger.info("Sending request to retrieve stub")
    status_code, result_dict = response_handler.get_response_data(charge_id)

    current_app.audit_logger.info("Request for charge id {}".format(charge_id))

    return json.dumps(result_dict, sort_keys=True, separators=(',', ':')), \
        status_code, {'Content-Type': 'application/json'}
