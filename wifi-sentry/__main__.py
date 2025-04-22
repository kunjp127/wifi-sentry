# main() entrypoint

import argparse
from . import APP_TITLE


# --- CLI Args
parser = argparse.ArgumentParser(
	prog=APP_TITLE
)
args = parser.parse_args()


print("ok")