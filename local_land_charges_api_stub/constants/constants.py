from local_land_charges_api_stub.app import app
import json
import requests
import time

from selenium import webdriver
import chromedriver_autoinstaller


class AddChargeConstants(object):
    STATUTORY_PROVISION=[]

    chromedriver_autoinstaller.install()

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    browser = webdriver.Chrome(chrome_options=options)

    url = "https://search-local-land-charges.service.gov.uk/statutory-provisions"
    
    browser.get(url)
    time.sleep(3)
    html = browser.execute_script("return document.getElementsByTagName('pre')[0].innerHTML")
    STATUTORY_PROVISION=json.loads(html)

    browser.close()
