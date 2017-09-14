from flask import current_app
from local_land_charges_api_stub.exceptions import ApplicationError
from local_land_charges_api_stub.utilities.charge_id import is_valid_charge_id
import os
import json


failed_status_codes = {"LLC-2": 404, "CLL-3": 422}


def get_response_data(charge_id):
    current_app.logger.info("retrieving json response for {}".format(charge_id))
    path = os.path.split(os.path.realpath(__file__))
    app_dir = os.path.split(path[0])[0]
    file_path = os.path.join(app_dir, "constants")
    if not is_valid_charge_id(charge_id):
        # CLL-3 is invalid charge ID response file
        file_name = "CLL-3"
    else:
        file_name = charge_id

    try:
        with open(os.path.join(file_path, "{}.json".format(file_name))) as json_response:
            return get_status_code(file_name), json.load(json_response)
    except FileNotFoundError as ex:
        file_name = "LLC-1"
        try:
            current_app.logger.info("retrieving json response for default charge {}".format(file_name))
            with open(os.path.join(file_path, "{}.json".format(file_name))) as json_response:
                return get_status_code(file_name), json.load(json_response)
        except Exception as ex:
            error_message = ex.errno
            raise ApplicationError(error_message, "E199", 500)


def get_status_code(charge_id):
    if charge_id in failed_status_codes:
        return failed_status_codes[charge_id]
    else:
        return 200
