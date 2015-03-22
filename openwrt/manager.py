from . import services, users, network, backup, portforwarding, dhcp
from .core import Shell, RPCProxy


class Manager:
    """
    A manager of a remote OpenWRT instance that provides more sophisticated management functionality that is not
    provided by the RPC interface directly.

    The functionality provided by this manager is delegated to several sub-managers available as attributes
    of this instance.
    """

    def __init__(self, hostname, username, password):

        # Core modules
        self._rpc = RPCProxy(hostname, username, password)
        self._shell = Shell(self._rpc)

        # Managers
        self._services = services.ServicesManager(self._shell)
        self._portforwarding_manager = portforwarding.PortForwardingManager(self._rpc, self._services)
        self._users = users.UserManager(self._shell, self._rpc)
        self._network = network.NetworkManager(self._rpc, self._services)
        self._backup = backup.BackupManager(self._shell)
        self._dhcp = dhcp.DHCPManager(self._shell, self._rpc)

    @property
    def port_forwarding(self):
        """
        Returns the manager of port forwarding rules.
        """
        return self._portforwarding_manager

    @property
    def services(self):
        """
        Returns the manager of running services.
        """
        return self._services

    @property
    def users(self):
        """
        Returns the manager of system users.
        """
        return self._users

    @property
    def network(self):
        """
        Returns the manager of network profiles.
        """
        return self._network

    @property
    def backup(self):
        """
        Returns the manager of backup operations.
        """
        return self._backup

    @property
    def dhcp(self):
        """
        Returns the manager of DHCP operations.
        """
        return self._dhcp