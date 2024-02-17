#!/bin/bash

docker build -t singularity:test . && docker run --rm singularity:test
