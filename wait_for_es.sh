#!/bin/bash

host="$1"

# First wait for ES to start...
response=$(curl --write-out %{http_code} --silent --output /dev/null "$host")
until [ "$response" = "200" ]; do
    response=$(curl --write-out %{http_code} --silent --output /dev/null "$host")
    >&2 echo "Waiting for ElasticSearch to boot up..."
    sleep 1
done

# next wait for ES status to turn to Yellow
health="$(curl -fsSL "$host/_cat/health?h=status")"
health="$(echo "$health" | sed -r 's/^[[:space:]]+|[[:space:]]+$//g')" # trim whitespace (otherwise we'll have "yellow ")
until [[ "$health" = 'yellow' || "$health" = "green" ]]; do
    health="$(curl -fsSL "$host/_cat/health?h=status")"
    health="$(echo "$health" | sed -r 's/^[[:space:]]+|[[:space:]]+$//g')" # trim whitespace (otherwise we'll have "yellow ")
    >&2 echo "Waiting for ElasticSearch to boot up..."
    sleep 1
done

>&2 echo "ElasticSearch is up"