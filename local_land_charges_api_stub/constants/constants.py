import json
import requests
import csv


class AddChargeConstants(object):

    url = 'https://search-local-land-charges.service.gov.uk/statutory-provisions'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/605.1.15'}
    response = requests.get(url, headers=headers)
    try:
        STATUTORY_PROVISION = json.loads(response.content)
    except json.JSONDecodeError:
        with open('local_land_charges_api_stub/constants/statutory_provisions.csv') as stat_prov_file:
            reader = csv.reader(stat_prov_file)
            STATUTORY_PROVISION = {rows[0]: rows[1] for rows in reader}
