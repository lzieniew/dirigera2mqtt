#!/bin/bash

SERVICE_NAME="dirigera2mqtt"
SERVICE_DIR="$HOME/.config/systemd/user/"
SERVICE_FILE="${SERVICE_DIR}${SERVICE_NAME}.service"
SCRIPT_DIR=$(realpath $(dirname "$0"))
VENV_PATH="${SCRIPT_DIR}/venv/bin/python" # Assuming the virtualenv is named 'venv'
SCRIPT_PATH="${SCRIPT_DIR}/main.py"

# Ensure the systemd user directory exists
mkdir -p ${SERVICE_DIR}

echo "Creating systemd user service file at ${SERVICE_FILE}"

cat <<EOF >${SERVICE_FILE}
[Unit]
Description=MQTT Service
After=network.target

[Service]
Type=simple
ExecStart=${VENV_PATH} ${SCRIPT_PATH}
Restart=always

[Install]
WantedBy=default.target
EOF

echo "Reloading systemd daemon for user..."
systemctl --user daemon-reload

echo "Enabling ${SERVICE_NAME} service to start on login..."
systemctl --user enable ${SERVICE_NAME}

echo "Starting ${SERVICE_NAME} service..."
systemctl --user start ${SERVICE_NAME}

echo "${SERVICE_NAME} user service setup complete. Virtual Environment activated."
