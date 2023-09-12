#!/bin/bash
set -e

source /app/conda/bin/activate fn_fastapi_services
cd /app/FN-FTA-Services
python -m py.test -v tests --disable-warnings