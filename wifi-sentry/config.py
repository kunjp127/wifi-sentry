# Class pertaining to application config


class WifiSentryConfig:
    """Application wide context specific configuration settings

    Raises:
            ValueError: Upon invalid configuration parameters
    """
    _known_hosts: dict = {}
    _interface: str
    debug = False

    def __init__(self, interface: str, known_hosts_file: str = None):
        """Create a config instance

        Args:
            interface (str): the BASE interface name to use
            known_hosts_file (str, optional): Known hosts config file path. Defaults to None.

        Raises:
            ValueError: Upon invalid configuration parameters
        """

        self._interface = interface

        self._known_hosts = {}
        if known_hosts_file:
            try:
                with open(known_hosts_file, "r") as file:
                    for line in file:
                        tokens = line.strip().split("=", 1)
                        mac = tokens[0]
                        hostname = tokens[1]
                        self._known_hosts[mac.lower()] = hostname
            except Exception as e:
                raise ValueError(f"Error reading known_hosts_file: {e}")

    def get_hostname(self, mac_address: str) -> str | None:
        """Get the known hostname for a given mac address, if any

        Args:
                mac_address (str): The mac address to get the known hostname for

        Returns:
                str | None: the hostname if it exists, otherwise None
        """
        return self._known_hosts.get(mac_address.lower(), None)

    def get_base_interface(self) -> str:
        """get the base network interface name

        Returns:
                str: the name of the base network interface
        """
        return self._interface

    def get_mon_interface(self) -> str:
        """get the monitor mode network interface name

        Returns:
                str: the name of the monitor mode network interface.
        """
        return self._interface + "mon"
