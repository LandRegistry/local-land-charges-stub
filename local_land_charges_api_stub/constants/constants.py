import urllib.request, json 
from flask import current_app

class AddChargeConstants(object):
    STATUTORY_PROVISION=[]
    with urllib.request.urlopen(current_app.config["STATUTORY_PROVISION_URL"]) as url:
        STATUTORY_PROVISION = json.loads(url.read().decode())
