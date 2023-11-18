#!/bin/bash

CONF_DIR=.
DATA_DIR=/mnt/bfd/models

docker run \
    -v "$CONF_DIR/models.json":/app/models.json \
    -v "$DATA_DIR":/models \
    model_manager  \
    /app/models.json  \
    /models

