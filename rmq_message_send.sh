#!/bin/bash
set -ex

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTDIR

# exec python -m service.Handler.message.test_send_message --es $RABBIT_HOST
if [ -f "$RABBIT_HOST" ]; then
    python service/Handler/message/test_send_message.py --es $RABBIT_HOST
else
    python service/Handler/message/test_send_message.py
fi