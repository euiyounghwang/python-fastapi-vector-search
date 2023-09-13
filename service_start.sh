#!/bin/bash
set -e

# vagrant ssh -- -L 9901:localhost:9201 -L 9000:localhost:9200 -L 5602:localhost:5601 -L 5603:localhost:5602 -L 5432:localhost:5432 -L 8080:localhost:8080 -L 8081:localhost:8081

# SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# cd $SCRIPTDIR
# source .venv/bin/activate

source /Users/euiyoung.hwang/opt/anaconda3/bin/activate fastapi_service
# source conda activate fastapi_service

# GUNICORN is a WSGI framework which, di per se, is not compatible with Fastapi, since Fastapi uses the ASGI standard (i.e. asynchronous). 
# This means that Gunicorn will have to use some layer of abstraction (uvicorn.workers.UvicornWorker) in order to communicate with the asynchronous call

# uvicorn main:app --reload --port=7000
# uvicorn main:app --reload --port=7000 --workers 4
uvicorn main:app --reload --host=0.0.0.0 --port=7000 --workers 4
# gunicorn main:app --reload --bind 0.0.0.0:7000 --workers 4

# gunicorn main:app --reload -k uvicorn.workers.UvicornWorker -b 0.0.0.0:7000 -w 4
# gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker -b 0.0.0.0:7000