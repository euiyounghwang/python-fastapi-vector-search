#!/bin/bash
set -e

cd /Users/euiyoung.hwang/ES/Python_Workspace/python-fastapi-vector-search
source ./.venv/bin/activate

# GUNICORN is a WSGI framework which, di per se, is not compatible with Fastapi, since Fastapi uses the ASGI standard (i.e. asynchronous). 
# This means that Gunicorn will have to use some layer of abstraction (uvicorn.workers.UvicornWorker) in order to communicate with the asynchronous call

# uvicorn main:app --reload --port=7000
uvicorn main:app --reload --port=7000 --workers 4
# gunicorn main:app --reload -k uvicorn.workers.UvicornWorker -b 0.0.0.0:7000 -w 4
# gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker -b 0.0.0.0:7000