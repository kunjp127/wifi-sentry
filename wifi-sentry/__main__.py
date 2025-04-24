# main() entrypoint

import argparse
from . import *
from .config import WifiSentryConfig
from .alert import ConsoleAlert, SMTPAlert
from scapy.all import sniff
from .mon import DefaultPacketHandler
import os


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
parser.add_argument(
    "--verbose",
    "-v",
    action="store_true",
    help="verbose/debug mode"
)
args = parser.parse_args()

# --- Quick czech
if os.getuid() != 0:
    print("run this as root")
    exit(1)

# --- App Context Config
config = WifiSentryConfig(IFACE_NAME, args.known_hosts)

if args.verbose:
    config.debug = True

print("Running on", config.get_mon_interface())

# --- Alerters config
alarms = [
    ConsoleAlert()#,
    # SMTPAlert(SMTP_HOST, SMTP_PORT, SMTP_USERNAME,
    #           SMTP_PASSWORD, SMTP_FROM, SMTP_TO)
]

print("Testing alarms")
for alarm in alarms:
    alarm.alert("no mac", "Test message")

print("test complete")

# --- Sniff, handle packets

print("Beginning to sniff")
handler = DefaultPacketHandler(config, alarms)
sniff(iface=config.get_mon_interface(), prn=handler.consume, store=0)
