#!/bin/bash

set -eu

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

#--platform linux/amd64
# VS Code : Remove -it
docker run --rm -it --name fn-flask-api-test --publish 1001:8080 --expose 8080 \
  -v "$SCRIPTDIR:/app/FN-FTA-Services/" \
  fn-flask-api:test
