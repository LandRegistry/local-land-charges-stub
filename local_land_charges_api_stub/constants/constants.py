import json
import time
import requests

class AddChargeConstants(object):

    url = 'https://search-local-land-charges.service.gov.uk/statutory-provisions'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/605.1.15'}
    response = requests.get(url, headers=headers)
    return json.loads(response.content)
