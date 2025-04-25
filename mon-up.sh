#!/bin/bash
airmon-ng check kill
airmon-ng start "$IFACE_NAME"