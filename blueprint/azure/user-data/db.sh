#!/bin/bash

# Source install_docker.sh to install Docker (assumes it's in the same directory)
source ./install_docker.sh

# Run the Qdrant container
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant
