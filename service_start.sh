#!/bin/bash
set -e

source ./.venv/bin/activate
# Start
uvicorn main:app --reload --port=7000