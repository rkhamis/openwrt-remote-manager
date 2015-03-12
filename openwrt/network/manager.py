from . import dhcpprofile, staticprofile
from .profile import NETWORK_PROFILE_PROTOCOL_DHCP, NETWORK_PROFILE_PROTOCOL_STATIC


def profile_from_dict(name, config_section):
    """
    Creates and returns a NetworkProfile out of the given profile name and configuration section parameters.
    """

    if 'proto' not in config_section:
        raise ValueError('config_section is not a configuration section of an interface')

    if config_section['proto'] == NETWORK_PROFILE_PROTOCOL_DHCP:
        return dhcpprofile.from_dict(name, config_section)
    elif config_section['proto'] == NETWORK_PROFILE_PROTOCOL_STATIC:
        return staticprofile.from_dict(name, config_section)
    else:
        raise RuntimeError('Unsupported protocol: {}'.format(config_section['proto']))


class NetworkManager:

    def __init__(self, rpc_proxy, service_manager):
        self._rpc = rpc_proxy
        self._services = service_manager

    @property
    def devices(self):
        """
        Returns a sequence of device (network interface) names.
        """
        return self._rpc.sys.net.devices()

    @property
    def profiles(self):
        """
        Returns a collection of network profiles as instances of DHCPNetworkProfile and StaticNetworkProfile.
        """
        return tuple(
            profile_from_dict(profile_name, config_section)
            for (profile_name, config_section) in self._rpc.uci.get_all('network').items()
            if config_section['.type'] == 'interface'
        )

    def delete_profile(self, network_profile):
        self._rpc.uci.delete('network', network_profile.name)

    def set_profile(self, network_profile):
        """
        Updates or adds a new a network profile and applies the changes to the network interfaces.

        Args:
            network_profile: an DHCPNetworkProfile or StaticNetworkProfile instance.
        """

        section_name = network_profile.name

        if section_name not in (profile.name for profile in self.profiles):
            assert self._rpc.uci.set('network', section_name, 'interface'), 'Failed to create a new network profile'

        for key, value in network_profile.to_dict().items():
            assert self._rpc.uci.set('network', network_profile.name, key, value), \
                'Failed to update a network profile'

        self._rpc.uci.commit('network')
        self._services.restart('network')

    def ping_host(self, host_name):
        """
        Pings an external host from the OpenWRT instance.

        Returns:
            True if the pinging was successful, False otherwise.
        """
        return self._rpc.sys.net.pingtest(host_name) == 0