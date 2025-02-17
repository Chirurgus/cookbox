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

# Fail on error

# Export environment variables from the .env file
export $(grep MYSQL_USER "$COOKBOX_DIR/.env")
export $(grep MYSQL_PASSWORD "$COOKBOX_DIR/.env")
export $(grep MYSQL_DATABASE "$COOKBOX_DIR/.env")

mkdir -p "$BACKUP_DIR/images"

docker exec $CONTAINER bash\
    -c 'mysqldump -u${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE}'\
    > "$BACKUP_DIR/cookbox.sql"

rsync --archive --delete "$COOKBOX_DIR/images" "$BACKUP_DIR/images"

chown -R $USER:$USER $BACKUP_DIR
