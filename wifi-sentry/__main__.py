# main() entrypoint

import argparse
from . import *
from .config import WifiSentryConfig
from .alert import ConsoleAlert, SMTPAlert


# --- CLI Args
parser = argparse.ArgumentParser(
    prog=APP_TITLE
)
parser.add_argument(
    "--known-hosts",
	"-k",
    type=str,
    metavar="FILE",
    help="Path to the file containing known hosts"
)
args = parser.parse_args()

# --- App Context Config
config = WifiSentryConfig(IFACE_NAME, args.known_hosts)

print("Running on", config.get_mon_interface())

# --- Alerters config
alarms = [
    ConsoleAlert(),
    SMTPAlert(SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM, SMTP_TO)
]

print("Testing alarms")
for alarm in alarms:
    alarm.alert("no mac", "Test message")

print("test complete")