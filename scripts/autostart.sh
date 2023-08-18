#!/bin/bash

# Navigate to the scripts directory.
cd "$(dirname "${BASH_SOURCE[0]}")"

# Navigate to ../api/main.py and get its full path
MAIN_PY_PATH="$( cd ../api && pwd )/main.py"

# Define variables
SERVICE_NAME="jayradar"
SERVICE_DESCRIPTION="A Vision Pipeline System"
EXECUTABLE_COMMAND="python3 $MAIN_PY_PATH"
USERNAME="$(whoami)"

# Create the systemd service file
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
echo "[Unit]" > $SERVICE_FILE
echo "Description=$SERVICE_DESCRIPTION" >> $SERVICE_FILE
echo "After=network.target" >> $SERVICE_FILE
echo "" >> $SERVICE_FILE
echo "[Service]" >> $SERVICE_FILE
echo "ExecStart=$EXECUTABLE_COMMAND" >> $SERVICE_FILE
echo "Restart=always" >> $SERVICE_FILE
echo "User=$USERNAME" >> $SERVICE_FILE
echo "" >> $SERVICE_FILE
echo "[Install]" >> $SERVICE_FILE
echo "WantedBy=multi-user.target" >> $SERVICE_FILE

# Enable and start the service
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

echo "Service $SERVICE_NAME has been set up and started."