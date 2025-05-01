#!/bin/bash

# Simple run script for faster testing
bash ./mon-up.sh
python3 -m wifi-sentry -k known_hosts.cfg $@
bash ./mon-down.sh