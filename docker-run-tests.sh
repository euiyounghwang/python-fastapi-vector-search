#!/bin/bash
set -e
echo "in.."
source /app/conda/bin/activate fn_fta_services
cd /app/FN-FTA-Services
# python -m py.test -v tests --disable-warnings
py.test -v tests --disable-warnings