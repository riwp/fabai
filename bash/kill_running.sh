#!/bin/bash

# Ports to check
ports=(5005 5006)

for port in "${ports[@]}"
do
    # Check if any process is running on the port and split PIDs into an array
    pids=$(sudo lsof -t -i:"$port")

    if [ -n "$pids" ]; then
        echo "Killing processes on port $port (PIDs: $pids)"
        
        # Loop through each PID and kill it
        for pid in $pids; do
            sudo kill -9 "$pid"
            echo "Killed process with PID: $pid"
        done
        
        echo "All processes on port $port killed."
    else
        echo "No process is running on port $port."
    fi
done
