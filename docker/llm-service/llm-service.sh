#!/bin/bash

docker run \
    --gpus all \
    -v /mnt/model_storage:/models \
    -p 8000:8000 \
    llm-service \
    /models \
    "$@"
