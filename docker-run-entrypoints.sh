#!/bin/bash
set -ex

#sleep 60

# --
# Poetry v.
# --
#source /app/poetry-venv/bin/activate
#cd /app/ES-Services
# poetry run python ./search-indexing-script.py --es $ES_HOST
#poetry run uvicorn main:app --reload --port=7000 --workers 4

# --
# Conda v.
# --
source /app/conda/bin/activate fn_fastapi_services
cd /app/FN-FTA-Services
exec uvicorn main:app --reload --host=0.0.0.0 --port=7000 --workers 4