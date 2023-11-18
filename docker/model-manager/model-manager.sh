#!/bin/bash

MODELS_STORAGE=/mnt/bfd/models
MODELS_CONFIG=./`dirname $0`

docker run \
    -v "$MODELS_CONFIG":/config \
    -v "$MODELS_STORAGE":/models \
    model-manager \
        /config/models.json \
        /models

