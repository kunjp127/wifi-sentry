import os

APP_TITLE: str = "wifi-sentry"
IFACE_NAME: str = os.getenv("IFACE_NAME", "wlp3s0") + "mon"