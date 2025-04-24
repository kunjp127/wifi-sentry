# main() entrypoint

import argparse
from . import APP_TITLE, IFACE_NAME
from .config import WifiSentryConfig


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


print("Running on", IFACE_NAME)
