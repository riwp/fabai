#!/bin/bash

# Define the services
services=("fabai_get_ai_insights.service")

# Loop through each service
for service in "${services[@]}"; do
  sudo systemctl stop "$service"
  echo "stopped service $service"
done

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload
