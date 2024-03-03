#!/bin/bash

# Variables
username="heletych"
process_name="ppurld"
user_to_check="berchtolde"
hostnames_file="/mnt/biocluster/praktikum/bioprakt/Data/hostnames"
remote_output_file="/tmp/ppurld.out"

# Iterate through each hostname in the hostnames file
while IFS= read -r hostname; do
    echo "Checking process on ${hostname}:"
    ssh "${username}@${hostname}.cip.ifi.lmu.de" "bash -s" < ./is_running.sh "$process_name" "$user_to_check"
    exit_status=$?

    if [ "$exit_status" -eq 1 ]; then
        echo "Process found on ${hostname}. Initiating SSH session and decoding the puzzle (ROT13)"
        decoded_url=$(ssh "${username}@${hostname}.cip.ifi.lmu.de" "grep -v '^#' $remote_output_file | tr 'A-Za-z' 'N-ZA-Mn-za-m'")
        
        # Download the data, filter out comments and extract columns 2 and 3
        wget -q -O - "$decoded_url" | grep -v '^#' | awk '{print $2, $3}' > visualization_data.txt
        
        echo "Data prepared for visualization. Calling Python script..."
        ./visualize_data.py visualization_data.txt
        
        break # Exit the loop after decoding and visualization
    fi
done < "$hostnames_file"

