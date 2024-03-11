REM local-land-charges-stub run script for Windows
REM assumes Python 3 installed and PATH configured
REM creates virtual environment and runs API
REM use ctrl-c to stop API and enter 'deactivate' to exit virtual environment

IF NOT EXIST ./venv (
python -m venv ./venv
)
CALL ./venv/Scripts/activate

pip install -r requirements.txt
pip install -r requirements_test.txt

set LOG_LEVEL=INFO
set COMMIT=LOCAL

python -m pytest