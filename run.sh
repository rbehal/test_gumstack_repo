#!/bin/bash

set -e
set -o pipefail

# Parse optional transport argument (default: streamable-http)
TRANSPORT="${1:-streamable-http}"

# Load environment variables from .env if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Disable Python output buffering
export PYTHONUNBUFFERED=1

# Activate venv if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "No active venv, creating .venv"
    uv sync -q
    source .venv/bin/activate
fi

# Run the server module directly
python -m my_example_server.server --transport "$TRANSPORT"