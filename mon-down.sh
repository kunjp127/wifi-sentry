#!/bin/bash
airmon-ng stop "${IFACE_NAME}mon"
#systemctl start NetworkManager