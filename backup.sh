#!/bin/bash

# Backup data from cookbox

# Location of the "active" .env file
# Check if the .env file path is provided as the second argument,
# otherwise use the default path
COOKBOX_DIR=$1

# Backup folder (with the suffix if present)
BACKUP_DIR=$2

# Docker container
CONTAINER=$3

USER=$4

mkdir -p "$BACKUP_DIR/data"

rsync --archive --delete "$COOKBOX_DIR/data" "$BACKUP_DIR/data"

chown -R $USER:$USER $BACKUP_DIR
