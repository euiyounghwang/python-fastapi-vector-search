#!/bin/bash
set -ex

#sleep 60
source /app/poetry-venv/bin/activate
cd /app/ES-Services
# poetry run python ./search-indexing-script.py --es $ES_HOST
poetry run uvicorn main:app --reload --port=7000 --workers 4