#!/bin/bash

set -eu

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

#--platform linux/amd64
# VS Code : Remove -it
# docker run --rm -it
docker run -i -t --name fn-vector-search-api-test \
  --publish 7002:8080 --expose 8080 \
  --network bridge \
  -e DATABASE_URL=postgresql://postgres:1234@host.docker.internal:15432/postgres \
  -e ES_HOST=http://host.docker.internal:9203 \
  -e RABBIT_HOST=host.docker.internal \
  -e PUBLISH_QUEUE=fastapi_publish_queue \
  -e RADIS_HOST=host.docker.internal \
  -e RADIS_PORT=6379 \
  -e REDIS_DATABASE=0 \
  -v "$SCRIPTDIR:/app/FN-FTA-Services/" \
  fn-vector-search-api:test
