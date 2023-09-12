#!/bin/bash

set -eu

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"


docker run --rm --platform linux/amd64 -it -d \
  --name fn-vector-search-api --publish 1000:7000 --expose 7000 \
  --network bridge \
  -v "$SCRIPTDIR:/app/FN-FTA-Services/" \
  fn-vector-search-api:es


