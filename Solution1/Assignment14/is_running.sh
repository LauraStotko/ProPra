#!/bin/bash

process_name=$1
username=$2

# Check if the process is running under the given username
if pgrep -u $username $process_name > /dev/null; then
    # Process is active
    exit 1
else
    # Process is not active
    exit 0
fi
