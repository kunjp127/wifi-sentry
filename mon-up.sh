#!/bin/bash
source ./.env
sudo airmon-ng check kill
sudo airmon-ng start "$IFACE_NAME"