#!/bin/bash

set -eu

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"


docker run --rm --platform linux/amd64 -it -d \
  --name fn-vector-search-api --publish 7001:7000 --expose 7000 \
  --network bridge \
  -e DATABASE_URL=postgresql://postgres:1234@host.docker.internal:15432/postgres \
  -e ES_HOST=http://host.docker.internal:9209 \
  -e RABBIT_HOST=host.docker.internal \
  -v "$SCRIPTDIR:/app/FN-FTA-Services/" \
  fn-vector-search-api:es


