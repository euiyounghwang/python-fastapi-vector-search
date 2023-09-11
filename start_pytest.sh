#!/bin/bash
set -e

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $SCRIPTDIR
# source .venv/bin/activate
source /Users/euiyoung.hwang/opt/anaconda3/bin/activate fastapi_service

# py.test -v tests
py.test -v --junitxml=test-reports/junit/pytest.xml --cov-report html --cov tests/
