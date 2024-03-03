#!/bin/bash

# To run this script use
# # ./ssh_copy_with_params.sh heletych topas

# Generate ssh key (if .ssh/id_rsa does not exist already)
# ssh-keygen

# Added ssh key on server
# ssh-copy-id heletych@topas.cip.ifi.lmu.de

# Assign the username and hostname to variables
username="$1"
hostname="$2.cip.ifi.lmu.de"

# Use the variables in the ssh-copy-id command
# ssh-copy-id "${username}@${hostname}" #only once

result=$(ssh ${username}@${hostname} 'cpu_cores=$(grep -c ^processor /proc/cpuinfo);load_one=$(cut -d " " -f 3 /proc/loadavg);load_percent=$(awk "BEGIN {printf \"%.2f\", (${load_one}/${cpu_cores})*100}"); echo "Current load (10-min average): ${load_percent}% of total CPU capacity (${cpu_cores} cores)."')
echo $result

# Example values in /proc/loadavg
# 0.03 0.01 0.00 average load over 1, 5, 10 minutes, where 1.0 is fully loaded (for 1-core system)
# 1/615 1438269 <runnable entities>/<total entities> <last processID used>

# Get the number of CPU cores (how many lines begin with processor)
# cpu_cores=$(grep -c ^processor /proc/cpuinfo)

# Get the 1-minute load average
# load_one=$(cut -d " " -f 3 /proc/loadavg) # d " " delimeter, -f 10-minute load

# Calculate load percentage
# Multiply load average by 100 to get a percentage
# Divide by number of CPU cores (awk is used for file processing)
# load_percent=$(awk "BEGIN {printf \"%.2f\", (${load_one}/${cpu_cores})*100}")

#echo "Current load (10-min average): ${load_percent}% of total CPU capacity (${cpu_cores} cores)."

