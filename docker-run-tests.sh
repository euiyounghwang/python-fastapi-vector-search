#!/bin/bash
set -e

sleep 60 
source /app/conda/bin/activate fn_fta_services
cd /app/FN-FTA-Services
# python -m py.test -v tests --disable-warnings
py.test -v tests --disable-warnings