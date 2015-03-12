from .profile import NetworkProfile, NETWORK_PROFILE_PROTOCOL_STATIC


class StaticNetworkProfile(NetworkProfile):
    """
    A NetworkProfile for a static network interface.

    Args:
        name (str): the name of the network profile
        interface_name (str): the name of the network interface to use
        ip4_address (str): the IPv4 address in dotted format
        ip6_address (str): the IPv6 address
        net_mask (str): the network mask
        ip4_gateway (str): the IPv4 address of the gateway
        ip6_gateway (str): the IPv6 address of the gateway
        dns (sequence of str): a sequence of DNS server addresses
        mtu (int): MTU
    """

    def __init__(self,
                 name,
                 interface_name,
                 ip4_address,
                 ip6_address=None,
                 net_mask=None,
                 ip4_gateway=None,
                 ip6_gateway=None,
                 dns=None,
                 mtu=None):

        if not ip4_address and not ip6_address:
            raise ValueError('ip4_address or ip6_address must be provided')

        if not ip6_address and not net_mask:
            raise ValueError('net_mask must be set if no ip6_address is set')

        NetworkProfile.__init__(self,
                                name=name,
                                protocol=NETWORK_PROFILE_PROTOCOL_STATIC,
                                interface_name=interface_name,
                                dns=dns,
                                mtu=mtu,
                                )

        self._ip4_address = ip4_address
        self._ip6_address = ip6_address
        self._net_mask = net_mask
        self._ip4_gateway = ip4_gateway
        self._ip6_gateway = ip6_gateway

    def updated(self,
                name=None,
                interface_name=None,
                ip4_address=None,
                ip6_address=None,
                netmask=None,
                ip4_gateway=None,
                ip6_gateway=None,
                dns=None,
                mtu=None):
        """
        Returns a mutated instance of this profile with the given parameters changed to the given values.
        """
        return StaticNetworkProfile(
            name=name or self.name,
            interface_name=interface_name or self.interface_name,
            ip4_address=ip4_address or self.ip4_address,
            ip6_address=ip6_address or self.ip6_address,
            net_mask=netmask or self.net_mask,
            ip4_gateway=ip4_gateway or self.ip4_gateway,
            ip6_gateway=ip6_gateway or self.ip6_gateway,
            dns=dns or self.dns,
            mtu=mtu or self.mtu,
        )

    @property
    def ip4_address(self):
        return self._ip4_address

    @property
    def ip6_address(self):
        return self._ip6_address

    @property
    def ip4_gateway(self):
        return self._ip4_gateway

    @property
    def ip6_gateway(self):
        return self._ip6_gateway

    @property
    def net_mask(self):
        return self._net_mask

    def to_dict(self):
        """
        Returns a dict with the configuration values as represented in OpenWRT's network configuration.
        """
        full_dict = {
            'ifname': self.interface_name,
            'proto': self.protocol,
            'netmask': self._net_mask,
            'gateway': self._ip4_gateway,
            'ip6addr': self._ip6_address,
            'ipaddr': self._ip4_address,
            'ip6gw': self._ip6_gateway,
            'mtu': self.mtu,
            'dns': self.dns,
        }
        return {k: v for k, v in full_dict.items() if v is not None and v is not ''}


def from_dict(name, values):
    """
    Returns a StaticNetworkProfile out of a profile name and the configuration section values.
    """
    return StaticNetworkProfile(
        name=name,
        interface_name=values['ifname'],
        ip4_address=values.get('ipaddr', None),
        ip6_address=values.get('ip6addr', None),
        net_mask=values.get('netmask', None),
        ip4_gateway=values.get('gateway', None),
        ip6_gateway=values.get('ip6gw', None),
        mtu=values.get('mtu', None),
        dns=values.get('dns', None),
    )