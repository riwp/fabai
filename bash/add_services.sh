#!/bin/bash

sudo systemctl daemon-reload

services=("fabai_aiwebui.service" "fabai_get_ai_insights.service")

# Loop through each service
for service in "${services[@]}"; do
  echo "Copying $service to /etc/systemd/system/"
  
  # Use full path for source files, change to your actual source directory if needed
  src_file="./$service"  # Assuming the script runs in the directory where the .service files are located

  # Check if the service file already exists in the destination
  if [ -f "/etc/systemd/system/$service" ]; then
    echo "$service already exists in /etc/systemd/system/, skipping copy."
  else
    sudo cp "$src_file" /etc/systemd/system/
    
    # Check if cp was successful
    if [ $? -eq 0 ]; then
      echo "$service copied successfully."
    else
      echo "Failed to copy $service. Please check your permissions or the destination."
      continue  # Skip to the next service if copying fails
    fi
  fi

  # Enable the service
  sudo systemctl enable "$service"
  if [ $? -eq 0 ]; then
    echo "$service enabled."
  else
    echo "Failed to enable $service."
  fi

  # Start the service
  sudo systemctl start "$service"
  if [ $? -eq 0 ]; then
    echo "$service started."
  else
    echo "Failed to start $service."
  fi
done

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Done. Now modify user configured in service files commands below:"
echo "sudo nano /etc/systemd/system/fabai_aiwebui.service"
echo "sudo nano /etc/systemd/system/fabai_get_ai_insights.service"
