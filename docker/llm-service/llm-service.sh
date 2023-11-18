#!/bin/bash

docker run \
    -v /mnt/bfd/models:/models \
    -p 8000:8000 \
    llm-service \
    /models/gpt2/11c5a3d5811f50298f278a704980280950aedb10
