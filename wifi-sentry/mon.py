from abc import ABC, abstractmethod
from typing import List
from .alert import AlertMethod
from .config import WifiSentryConfig
import numpy as np
from scapy.all import *
from scapy.layers.dot11 import *
from sklearn.ensemble import IsolationForest
from . import logger


# This module defines a handler to sniff packets


class PacketHandler(ABC):
    """A class type to process incoming packets
    """

    def __init__(self, config: WifiSentryConfig, alarms: List[AlertMethod] = []):
        """Create a Packet Handler message

        Args:
            config (WifiSentryConfig): Context config
            alarms (List[AlertMethod]): List of alarms to trigger upon detection
        """
        self._config = config
        self._alarms = alarms

    def alert(self, mac: str, message: str):
        """Send all alerts

        Args:
            mac (str): Alarm MAC
            message (str): Alarm message
        """
        for alarm in self._alarms:
            alarm.alert(mac, message)

    @abstractmethod
    def consume(self, pkt: Packet):
        """Process a packet

        Args:
            pkt (🤷): The singular packet to process
        """
        pass


class DefaultPacketHandler(PacketHandler):
    """Determines if packets are suspicious, alerts if so
    """

    # Store this number of RSSI samples per mac
    RSSI_WINDOW_SIZE = 5
    # Require this many samples to train the AI model
    MIN_BASELINE_SAMPLES = 5
    # Manual fallback threshold
    RSSI_THRESHOLD_DBM = 15

    # samples of RSSI data
    _rssi_history = {}
    # Collection of ML models per-mac
    _mac_models = {}
    # Averages collected during training period per-max
    _baseline_means = {}

    def _get_rssi(self, pkt: Packet) -> int:
        """Extract the RSSI/Signal strength from the scapy packet

        Args:
            pkt (Packet): Scapy packet

        Returns:
            int: Signal strength in DBM
        """
        if pkt.haslayer(RadioTap):
            return pkt[RadioTap].dBm_AntSignal

    def _rssi_get_mean_var(self, mac: str) -> tuple:
        """This calculates the mean and variance of the RSSI readings for the given MAC address

        Args:
            mac (str): mac addr

        Returns:
            tuple: Tuple: (mean, variance)
        """

        rssi_vals = np.array(self._rssi_history[mac])
        mean = np.mean(rssi_vals)
        var = np.var(rssi_vals)
        return (mean, var)

    def _train_model(self, mac):
        """Train le model

        Args:
            mac (str): The mac to train the model for
        """
        # Get statistical data
        features = self._rssi_get_mean_var(mac)

        # Use an isolation forest b/c
        model = IsolationForest(contamination="auto")
        model.fit([features])

        # Add this model to the list
        self._mac_models[mac] = model

        # Store average RSSI for manual threshold
        self._baseline_means[mac] = features[0]  # store mean RSSI

        nickname = self._config.get_hostname(mac)
        logmac = nickname if nickname else mac

        logger.log(logmac, "trained model")

    def consume(self, pkt: Packet):
        """Process a packer

        Args:
            pkt (Packet): the packet to process
        """

        # Get SOURCE MAC address specifically
        if pkt.haslayer(Dot11):  # wifi frame
            mac = pkt[Dot11].addr2
        else:  # or drop
            return

        # If pkt is garbled
        if mac is None:
            return

        # Get known hostname if possible
        nickname = self._config.get_hostname(mac)
        logmac = nickname if nickname else mac

        # Get rssi
        rssi = self._get_rssi(pkt)
        if rssi is None:
            return

        # Log power level if debug on
        if self._config.debug == True:
            logger.log(logmac, rssi)

        # Initialize history window for new MAC
        if mac not in self._rssi_history:
            self._rssi_history[mac] = []

        # Update RSSI history
        self._rssi_history[mac].append(rssi)
        self._rssi_history[mac] = self._rssi_history[mac][-self.RSSI_WINDOW_SIZE:]

        # train model if sufficient samples
        if mac not in self._mac_models and len(self._rssi_history[mac]) >= self.MIN_BASELINE_SAMPLES:
            self._train_model(mac)
            return

        # detect spoofs if sufficient data has accumulated
        if mac in self._mac_models and len(self._rssi_history[mac]) == self.RSSI_WINDOW_SIZE:
            # Get stat data/mean
            features = self._rssi_get_mean_var(mac)
            mean_rssi = features[0]

            # Perform ML prediction
            ml_prediciton = self._mac_models[mac].predict(
                [features])[0]  # 1 = normal, -1 is not normal
            # If the model is not normal or the threshold is exceeded, alert
            if (ml_prediciton == -1 or abs(
                    mean_rssi - self._baseline_means[mac]) > self.RSSI_THRESHOLD_DBM):
                # Alert! Alert! Alert!
                for a in self._alarms:
                    nickname = self._config.get_hostname(mac)

                    if nickname:
                        a.alert(logmac, f"Someone is spoofing {nickname}!")
                    else:
                        a.alert(logmac, f"Someone is spoofing this device!")
