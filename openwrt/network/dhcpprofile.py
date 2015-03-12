from .profile import NETWORK_PROFILE_PROTOCOL_DHCP, NetworkProfile


class DHCPNetworkProfile(NetworkProfile):

    def __init__(self, name, interface_name, mtu=None):
        NetworkProfile.__init__(self,
                                name=name,
                                protocol=NETWORK_PROFILE_PROTOCOL_DHCP,
                                interface_name=interface_name,
                                mtu=mtu
                                )

    def updated(self, name=None, interface_name=None, mtu=None):
        """
        Returns a mutated instance of this profile with the given parameters changed to the given values.
        """
        return DHCPNetworkProfile(
            name=name or self.name,
            interface_name=interface_name or self.interface_name,
            mtu=mtu or self.mtu
        )

    def to_dict(self):
        """
        Returns a dict with the configuration values as represented in OpenWRT's network configuration.
        """
        full_dict = {
            'proto': self.protocol,
            'ifname': self.interface_name,
            'mtu': self.mtu,
            'dns': self.dns,
        }
        return {k: v for (k, v) in full_dict.items() if v is not None and v is not ''}


def from_dict(name, values):
    """
    Parses a DHCPNetworkProfile out of a profile name and configuration section values.
    """
    return DHCPNetworkProfile(
        name=name,
        interface_name=values['ifname'],
        mtu=values.get('mtu', None),
    )