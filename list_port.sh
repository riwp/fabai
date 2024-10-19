#!/bin/bash

# Check if port number is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <port-number>"
  exit 1
fi

# Run the netstat command with the provided port number
sudo netstat -tuln | grep ":$1"

# Check if the command was successful
if [ $? -eq 0 ]; then
  echo "Port $1 is in use."
else
  echo "No services running on port $1."
fi

