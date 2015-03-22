import collections

class DHCPLease(collections.namedtuple('DHCPLease',
                                                field_names=('timestamp', 'ip4_address', 'mac_address',))):
    """
    An immutable DHCP lease.
    """

    @staticmethod
    def from_dict(dict_obj):
        """
        Unpacks values from a dict of optional values. Nonexistent values will be set to None.

        Metadata key-value pairs which should exist in the input dict object should be prefixed by a '.' character,
        like '.name' and '.index'. These metadata keys will be translated to ones with the prefix 'meta_' instead like
        'meta_name' and 'meta_index'.
        """
        return DHCPLease(*(
            dict_obj.get(field_name.replace('meta_', '.'), None) for field_name in DHCPLease._fields))

    def _to_dict(self):
        return {name.replace('meta_', '.'): getattr(self, name) for name in self.field_names}

    @property
    def field_names(self):
        return self._fields

    @property
    def non_meta_field_names(self):
        return tuple(field_name for field_name in self.field_names if not field_name.startswith('meta_'))

    def updated(self, **kwargs):
        """
        Returns a mutated instance of this DHCPLease according to the provided keyword arguments.
        """
        values = self._to_dict()
        values.update(kwargs)
        return DHCPLease.from_dict(values)

class DHCPManager:
    """
    Manager of DHCP an OpenWRT installation.
    """

    def __init__(self, shell, rpc_proxy):
        self._shell = shell
        self._rpc_proxy = rpc_proxy

    def __lease_path(self):
        dnsmasq = {'leasefile': '/tmp/dhcp.leases'}
        dhcpconfig = self._rpc_proxy.uci.get_all('dhcp')
        for dhcp in dhcpconfig.values():
            if not dhcp.get('.type') == 'dnsmasq':
                continue
            for key, value in dhcp.iteritems():
                dnsmasq[key] = value
        leasefile = dnsmasq['leasefile']
        return leasefile 

    @property
    def current_leases(self):
        """
        Returns a collection of current DHCP leases
        """
        path = self.__lease_path()
        dhcpleases = self._shell.execute("cat %s" % path).splitlines()
        leases = list()
        for lease in dhcpleases:
            timestamp, mac_address, ip4_address=lease.split()[:3]
            leases.append({'timestamp': timestamp, 'ip4_address': ip4_address, 'mac_address': mac_address})
        result = tuple(DHCPLease.from_dict(lease) for lease in leases)
        return result

