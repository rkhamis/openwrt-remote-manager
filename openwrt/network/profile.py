
from . import util

NETWORK_PROFILE_PROTOCOL_DHCP = 'dhcp'
NETWORK_PROFILE_PROTOCOL_STATIC = 'static'


class NetworkProfile:
    """
    A NetworkProfile is a configuration section in OpenWRT's /etc/config/network file.

    See: http://wiki.openwrt.org/doc/uci/network
    """

    def __init__(self, name, interface_name, protocol, dns=None, mtu=None):

        if dns and not util.is_sequence(dns):
            raise ValueError('dns can only be None or a sequence of IP addresses')

        self._name = name
        self._interface_name = interface_name
        self._protocol = protocol
        self._mtu = mtu
        self._dns = dns

    @property
    def name(self):
        return self._name

    @property
    def protocol(self):
        return self._protocol

    @property
    def interface_name(self):
        return self._interface_name

    @property
    def dns(self):
        return self._dns

    @property
    def mtu(self):
        return self._mtu

    def __str__(self):
        return '{} on {}'.format(self.name, self.interface_name)