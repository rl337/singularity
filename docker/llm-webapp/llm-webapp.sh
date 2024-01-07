#!/bin/bash

APPLICATION_NAME=llm-frontend

RUNNING=$(docker inspect --format="{{ .State.Running }}" "$APPLICATION_NAME" 2>/dev/null)
case "$RUNNING" in
    "true")
        echo "Stopping and removing existing instance"
        docker stop "$APPLICATION_NAME"
        docker rm "$APPLICATION_NAME"
        ;;
    "false")
        echo "Removing dead instance"
        docker rm "$APPLICATION_NAME"
        ;;
    *)
        echo "No previous instance"
        ;;
esac

docker run --detach --name="$APPLICATION_NAME" -p 4000:80 llm-webapp:latest
