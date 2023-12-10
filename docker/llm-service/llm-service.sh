#!/bin/bash

docker run \
    -v /mnt/model_storage:/models \
    -p 8000:8000 \
    llm-service \
    /models \
    "$@"
