import os
from dotenv import load_dotenv


load_dotenv()


APP_TITLE: str = "wifi-sentry"
IFACE_NAME: str = os.getenv("IFACE_NAME", "wlp3s0")
SMTP_HOST: str = os.getenv("SMTP_HOST", None)
SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", None)
SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", None)
SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
SMTP_FROM: str = os.getenv("SMTP_FROM", "")
SMTP_TO: str = os.getenv("SMTP_TO", "root@localhost")
