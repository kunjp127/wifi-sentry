# main() entrypoint

import argparse
from . import APP_TITLE, IFACE_NAME


# --- CLI Args
parser = argparse.ArgumentParser(
	prog=APP_TITLE
)
args = parser.parse_args()


print("Running on", IFACE_NAME)