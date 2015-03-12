
from .core.rpcproxy import AuthenticationError
from .portforwarding import PortForwardingRule
from .network import StaticNetworkProfile, DHCPNetworkProfile


def create_manager(hostname, username, password):
    """
    Creates and returns a manager for the OpenWRT instance for the specified information.

    Args:
        hostname: the hostname to the OpenWRT instance
        username: the configured Luci username
        password: the configured luci password

    Raises:
        AuthenticationError: any call can raise this when authentication fails
    """
    import manager
    return manager.Manager(hostname, username, password)


__all__ = [
    'create_manager',
    'AuthenticationError',
    'PortForwardingRule',
    'StaticNetworkProfile',
    'DHCPNetworkProfile',
]
