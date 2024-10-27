#!/bin/bash

# Define the ports to check
ports=(5005 5006)

# Loop through the ports and check each one
for port in "${ports[@]}"; do
  #echo "Checking port $port..."
  sudo netstat -tuln | grep ":$port"

  # Check if the command was successful
  if [ $? -eq 0 ]; then
    echo "Port $port is in use."
  else
    echo "No services running on port $port."
  fi
  #echo "------------------------"
done
