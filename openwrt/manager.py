from openwrt import shell, services
import rpcproxy
import portforwarding


class Manager:
    """
    A manager of a remote OpenWRT instance that provides more sophisticated management functionality that is not
    provided by the RPC interface directly.
    """

    def __init__(self, hostname, username, password):
        self._rpc = rpcproxy.create(hostname, username, password)
        self._shell = shell.ShellManager(self._rpc)
        self._services = services.ServicesManager(self._shell)
        self._portforwarding_manager = portforwarding.PortForwardingManager(self._rpc, self._services)

    @property
    def rpc(self):
        """
        Returns a proxy to OpenWRT's Luci-exported JSONRPC interface.

        For more information about the JSONRPC interface, see:
        http://luci.subsignal.org/trac/wiki/Documentation/JsonRpcHowTo

        Usage:
            Returned object act as a direct proxy and can be used directly to call exported
            methods on all the available libraries.

            >>> manager = ...
            >>> for path in manager.rpc.fs.dir():
            >>>     print(path)
            :return:
        """
        return self._rpc

    @property
    def port_forwarding(self):
        return self._portforwarding_manager

    @property
    def shell(self):
        return self._shell

    @property
    def services(self):
        return self._services