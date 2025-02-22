#!/bin/bash

# Default to local if no environment specified
ENV=${1:-local}

# Export the environment
export ENV=$ENV

# Run docker-compose
docker compose up -d 