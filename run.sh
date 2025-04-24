#!/bin/bash

# Simple run script for faster testing
bash ./mon-up.sh
sudo .venv/bin/python3 -m wifi-sentry -k known_hosts.cfg $@
bash ./mon-down.sh