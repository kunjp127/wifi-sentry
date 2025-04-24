from abc import ABC, abstractmethod
from datetime import datetime
import smtplib
import ssl
from . import logger
import os
import time

# Classes pertaining to the alerting of a detection


class AlertMethod(ABC):
    """Provides an interface to define custom alert types; i.e console and email.
    """
    @abstractmethod
    def alert(self, mac: str, message: str) -> None:
        """Send an alert

        Args:
            mac (str): The mac address this alert is for
            message (str): The message to send
        """
        pass


class ConsoleAlert(AlertMethod):
    """Send an alert via stdout
    """

    def alert(self, mac: str, message: str) -> None:
        logger.log(mac, message)


class SMTPAlert(AlertMethod):
    """Send an alert via SMTP email
    """

    def __init__(self, smtp_host: str, smtp_port: int, smtp_username: str, smtp_password: str, from_email: str, to_email: str):
        # initialize SMTP alert with necessary credentials and email info
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.to_email = to_email

    def alert(self, mac: str, message: str) -> None:
        # create email subject and body for alert
        subject = f"Suspicious behavior for {mac}"
        body = f"[{logger.get_timestamp()}] [{mac}] {message}"

        # construct email message
        msg = f"""From: {self.from_email}
To: {self.to_email}
Subject: {subject}

{body}
"""
        print("Mailing", self.to_email)

        try:
            # Shut down mon
            os.system("sudo bash mon-down.sh")

            # Wait for internet
            time.sleep(10)
            
            # connect to SMTP server and send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                # server.set_debuglevel(1)  # for debugging
                # server.connect(self.smtp_host, self.smtp_port)  # this messes up ehlo
                server.ehlo()  # why is this necessary
                # start TLS with context
                server.starttls(context=ssl.create_default_context())
                server.ehlo()  # re-identify after TLS
                # login to SMTP
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.from_email, self.to_email,
                                msg)  # send the email
        except Exception as e:
            # print error if email sending fails
            print(f"failed to send email alert: {e}")
        finally:
            os.system("sudo bash mon-up.sh")
            # Wait for spin-up
            time.sleep(15)
