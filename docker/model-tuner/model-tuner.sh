#!/bin/bash

MODELS_STORAGE=/mnt/model_storage
DATA_STORAGE=/mnt/bfd/datasets
MODELS_CONFIG=./`dirname $0`

docker run \
    --gpus all \
    -v "$MODELS_CONFIG":/config \
    -v "$MODELS_STORAGE":/models \
    -v "$DATA_STORAGE":/data \
    model-tuner:latest \
        /models/gpt2-medium \
        /data/singularity_math.tgz \
        /models/gpt2-singularity

