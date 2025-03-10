REM local-land-charges-stub run script for Windows
REM assumes Python 3 installed and PATH configured
REM creates virtual environment and runs API
REM use ctrl-c to stop API and enter 'deactivate' to exit virtual environment

IF NOT EXIST ./venv (
python -m venv ./venv
)
CALL ./venv/Scripts/activate

pip install -r requirements.txt

python --version 

set LOG_LEVEL=INFO
set COMMIT=LOCAL
set FLASK_APP=local_land_charges_api_stub/main.py

python -m flask run