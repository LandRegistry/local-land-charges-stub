#!/bin/bash

# Ensure virtual environment is set up
if [ ! -d "venv" ]; then
    echo "venv folder does not exist, creating it..."
    python3 -m venv ./venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt
pip3 install -r requirements_test.txt

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
