#!/bin/bash
source ./.env
sudo airmon-ng stop "${IFACE_NAME}mon"
sudo systemctl start NetworkManager