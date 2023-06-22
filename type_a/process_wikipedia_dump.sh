#!/bin/bash

DATA_DIR="/mnt/bfd/raw/wikipedia/"
VENV_DIR=venv-obsidian


INPUT_FILE="$DATA_DIR/2023-04-22/enwiki-20230420-pages-articles.xml.bz2"
NUM_SHARDS=4
PARALLEL_JOBS=4

PYTHON=./$VENV_DIR/bin/python3
PYTHON_PATH=.

export PYTHON PYTHON_PATH

seq 0 $((NUM_SHARDS - 1)) | xargs -I{} -P $PARALLEL_JOBS \
    "$PYTHON" -m singularity.slurpy \
        --shards=$NUM_SHARDS \
        --shard-no={} \
        --input-file=$INPUT_FILE

