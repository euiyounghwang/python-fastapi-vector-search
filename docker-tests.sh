#!/bin/bash

set -eu

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

#--platform linux/amd64
# VS Code : Remove -it
# docker run --rm -it
docker run --rm -it --name fn-vector-search-api-test \
  --publish 7002:8080 --expose 8080 \
  -e DATABASE_URL=postgresql://postgres:1234@host.docker.internal:15432/postgres \
  -e ES_HOST=http://host.docker.internal:9209 \
  --network bridge \
  -v "$SCRIPTDIR:/app/FN-FTA-Services/" \
  fn-vector-search-api:test
