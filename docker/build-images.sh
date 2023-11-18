#!/bin/bash

CONTAINERS_DIR=`dirname $0`


if [ "X$1" == "X" ]; then
    CONTAINERS=`find "$CONTAINERS_DIR" -type d | xargs -Ixxx basename xxx | grep -v "^\."`
else
    CONTAINERS=`find "$CONTAINERS_DIR" -type d | xargs -Ixxx basename xxx | grep -v "^\." | grep "$1"`
fi


for CONTAINER in $CONTAINERS; do
    echo "$CONTAINER"
    docker build -t "$CONTAINER" "$CONTAINERS_DIR/$CONTAINER"
done
