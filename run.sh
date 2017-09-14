# For Flask CLI

virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt


export FLASK_APP=local_land_charges_api-stub/main.py
export FLASK_DEBUG=1
# For Python
export PYTHONUNBUFFERED=yes
# For gunicorn
export PORT=9080
# For app's config.py
export FLASK_LOG_LEVEL=DEBUG
export LOG_LEVEL=DEBUG
export COMMIT=LOCAL
export APP_NAME=local-land-charges-api-stub

export PYTHONPATH='.'

# Run the app
make run