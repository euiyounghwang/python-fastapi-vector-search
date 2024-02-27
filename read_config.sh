#!/bin/bash
set -e

function get_value_from_yaml()
{
    #cat ./config.yaml | jq .app.es.es_host
    ES_HOST=$(cat ./config.yaml | jq .app.es.omni_es_host)
    ES_HOST=$(sed -e 's/^"//' -e 's/"$//' <<< $ES_HOST)
    echo 'get_value_from_yaml -> ' ${ES_HOST}
}