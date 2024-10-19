#!/bin/bash

# Define the services
services=("fabai_aiwebui.service" "fabai_get_ai_insights.service")

# Loop through each service
for service in "${services[@]}"; do
  echo "Checking status for $service..."
  sudo systemctl status "$service"  # Execute the command to display the status
  echo  # Add a newline for better readability
done
