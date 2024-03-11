#!/bin/bash

# Check to make sure that the venv folder is present, if not, create it
if [ ! -d "venv" ] 
then
    echo "Folder does not exist, creating folder"
    mkdir venv
fi

python3 -m venv ./venv 
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt
pip3 install -r requirements_test.txt
pip install --force-reinstall urllib3==2.2.1

# Set environment variables necessary for testing
export FLASK_APP=local_land_charges_api-stub/main.py
export FLASK_DEBUG=1
export PYTHONUNBUFFERED=yes
export FLASK_LOG_LEVEL=DEBUG
export LOG_LEVEL=DEBUG
export COMMIT=LOCAL
export APP_NAME=local-land-charges-api-stub
export PYTHONPATH='.'

# Run unit tests
make unittest

deactivate
