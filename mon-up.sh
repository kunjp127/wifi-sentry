#!/bin/bash
source ./.env
sudo airmon-ng start "$IFACE_NAME"