#!/bin/bash

SCRIPT_DIR=`dirname $0`

cd "$SCRIPT_DIR/.."

SINGULARITY_DIR="."
CONTAINERS_DIR="$SINGULARITY_DIR/docker"

ALL_CONTAINERS=`find "$CONTAINERS_DIR" -maxdepth 1 -type d | xargs -Ixxx basename xxx | grep -v '^\.\|^config$'`
if [ "X$1" == "X" ]; then
    CONTAINERS="$ALL_CONTAINERS"
else
    CONTAINERS=`echo "$ALL_CONTAINERS" | grep "$1"`
fi

if [ "X$NOCACHE" != "X" ]; then
    OTHER_ARGS="--no-cache"
fi

CONFIG_DIR="$SINGULARITY_DIR/config"
for CONTAINER in $CONTAINERS; do
    echo "$CONTAINER"
    CONTAINER_DIR="$CONTAINERS_DIR/$CONTAINER"
    docker build $OTHER_ARGS \
        --build-arg PROJECT_DIR="$CONTAINER_DIR" \
        --build-arg CONFIG_DIR="$CONFIG_DIR" \
        -t "$CONTAINER" \
        -f "$CONTAINER_DIR/Dockerfile" \
        .
done
