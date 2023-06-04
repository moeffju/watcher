#!/bin/bash

SCRIPT_DIR=$(realpath $(dirname $0))
SOURCE_FOLDER="$SCRIPT_DIR/source"
DESTINATION_FOLDER="$SCRIPT_DIR/destination"
DOCKER_IMAGE="watcher:latest"

docker run -v "$SOURCE_FOLDER:/source" -v "$DESTINATION_FOLDER:/destination" "$DOCKER_IMAGE"
