class AddResponses(object):

    add_valid_response = {
        "land-charge-id": "LLC-01",
        "registration-date": "2017-08-04",
        "version-id": 50
    }

    @staticmethod
    def add_vary_cancel_response(charge_id, version_id):
        status_code = 201
        if charge_id == "LLC-10" and version_id == "3":
            response = {
                "error_code": 404,
                "error_message": "ID 'LLC-10' cannot be found"
            }
            status_code = 404
        elif charge_id == "LLC-10":
            response = {
                "error_code": "E010",
                "error_message": "Version ID submitted is not latest version"
            }
            status_code = 422
        elif charge_id == "LLC-99":
            response = {
                "error_code": "E400",
                "error_message": {
                    "details": [{
                        "location": "$.item.end-date",
                        "error_message": "Cannot amend a cancelled record"
                    }],
                    "error": "Charge is invalid"
                }
            }
            status_code = 400
        else:
            version_id = int(version_id) + 1
            response = {
                "land-charge-id": charge_id,
                "registration-date": "2017-08-11",
                "version-id": version_id
            }
        return status_code, response

    @staticmethod
    def cancel_charge_response(charge_id, version_id):
        status_code = 201
        version_id = int(version_id) + 1
        response = {
            "land-charge-id": charge_id,
            "registration-date": "2017-03-17",
            "version-id": version_id

        }
        return status_code, response
