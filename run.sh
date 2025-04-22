#!/bin/bash

# Simple run script for faster testing

bash ./mon-up.sh
source ./.env && python -m wifi-sentry
bash ./mon-down.sh