
import collections


class PortForwardingRule(collections.namedtuple('PortForwardingRule',
                                                field_names=('name', 'src', 'src_ip', 'src_dip', 'src_dport',
                                                             'dest', 'dest_ip', 'dest_port', 'proto',
                                                             'meta_name', 'meta_index', 'meta_anonymous'))):
    """
    An immutable port-forwarding rule.
    """

    @staticmethod
    def from_dict(dict_obj):
        """
        Unpacks values from a dict of optional values. Nonexistent values will be set to None.

        Metadata key-value pairs which should exist in the input dict object should be prefixed by a '.' character,
        like '.name' and '.index'. These metadata keys will be translated to ones with the prefix 'meta_' instead like
        'meta_name' and 'meta_index'.
        """
        return PortForwardingRule(*(
            dict_obj.get(field_name.replace('meta_', '.'), None) for field_name in PortForwardingRule._fields
        ))

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
        Returns a mutated instance of this PortForwardingRule according to the provided keyword arguments.
        """
        values = self._to_dict()
        values.update(kwargs)
        return PortForwardingRule.from_dict(values)

    @staticmethod
    def create(name, src=None, src_ip=None, src_dip=None, src_dport=None, dest=None, dest_ip=None,
               dest_port=None, proto=None):
        """
        Creates and returns a new instance.
        """

        return PortForwardingRule(name=name, src=src, src_ip=src_ip, src_dip=src_dip, src_dport=src_dport,
                                  dest=dest, dest_ip=dest_ip, dest_port=dest_port, proto=proto,
                                  meta_name=None, meta_index=None, meta_anonymous=None)


class PortForwardingManager:

    def __init__(self, rpc_proxy, service_manager):
        self._rpc = rpc_proxy
        self._services = service_manager

    @property
    def all(self):
        """
        Returns a collection of PortForwardingRule instances.
        """
        return tuple(PortForwardingRule.from_dict(rule) for rule in
                     self._rpc.uci.get_all('firewall').values() if rule['.type'] == 'redirect')

    def delete(self, rule):
        """
        Deletes a specific port forwarding rule.

        Args:
            rule: a PortForwarding instance or a meta_name or a meta_index of one.
        """
        if isinstance(rule, PortForwardingRule):
            return self.delete(rule.meta_name)
        elif isinstance(rule, int):
            self._rpc.uci.delete('firewall', '@redirect[{}]'.format(rule))
            self._commit_config_and_restart_firewall_service()
        elif isinstance(rule, (str, unicode)):
            self._rpc.uci.delete('firewall', rule)
            self._commit_config_and_restart_firewall_service()
        else:
            raise ValueError('Invalid argument')

    def update(self, rule):
        """
        Updates the state of the given port forwarding rule according to the possibly-changed state reflected
        in the rule argument.

        Args:
            rule: a PortForwardingRule instance
        """
        assert rule.meta_name, 'The rule must have an associated meta_name'
        for field_name in rule.non_meta_field_names:
            value = getattr(rule, field_name)
            if value:
                assert(self._rpc.uci.set('firewall', rule.meta_name, field_name, value))
            elif self._rpc.uci.get('firewall', rule.meta_name, field_name):
                assert(self._rpc.uci.delete('firewall', rule.meta_name, field_name))

        self._commit_config_and_restart_firewall_service()

    def add(self, new_rule):
        """
        Adds a newly-created PortForwardingRule instance to the OpenWRT firewall.

        Args:
            new_rule: a PortForwardingRule created by a call to PortForwardingRrule.create(.)

        Returns:
            The created rule updated with a meta_key and a meta_index.
        """
        new_key = self._rpc.uci.add('firewall', 'redirect')
        for field_name in new_rule.field_names:
            if getattr(new_rule, field_name, None):
                self._rpc.uci.set('firewall', new_key, field_name, getattr(new_rule, field_name))

        self._commit_config_and_restart_firewall_service()
        return PortForwardingRule.from_dict(self._rpc.uci.get_all('firewall', new_key))

    def _commit_config_and_restart_firewall_service(self):
        self._rpc.uci.commit('firewall')
        self._services.restart('firewall')
