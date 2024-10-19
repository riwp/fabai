#!/bin/bash

# Define the services
services=("fabai_aiwebui.service" "fabai_get_ai_insights.service")

# Loop through each service, stop and disable it, then remove it
for service in "${services[@]}"; do
  echo "Processing $service..."

  # Check if the service is loaded
  if systemctl list-units --full -all | grep -q "$service"; then
    echo "Stopping $service..."
    sudo systemctl stop $service

    echo "Disabling $service..."
    sudo systemctl disable $service
  else
    echo "$service is not loaded or active, skipping stop and disable."
  fi

  # Check if the service file exists before trying to remove it
  if [ -f "/etc/systemd/system/$service" ]; then
    echo "Removing $service..."
    sudo rm /etc/systemd/system/$service
  else
    echo "$service file does not exist, skipping removal."
  fi

  echo "Reloading systemd daemon..."
  sudo systemctl daemon-reload

  echo "$service has been processed."
done

echo "Done."
