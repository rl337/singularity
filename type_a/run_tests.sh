#!/bin/bash

docker build -t singularity:test . && docker run --gpus all --rm singularity:test
