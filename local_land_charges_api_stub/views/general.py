from flask import request, Blueprint, Response
from flask import current_app
import json


# This is the blueprint object that gets registered into the app in blueprints.py.
general = Blueprint('general', __name__)


@general.route("/health")
def check_status():
    return Response(response=json.dumps({
        "app": current_app.config["APP_NAME"],
        "status": "OK",
        "headers": request.headers.to_wsgi_list(),
        "commit": current_app.config["COMMIT"]
    }), mimetype='application/json', status=200)
