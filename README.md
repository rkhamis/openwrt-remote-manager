# OpenWRT Remote Manager #

A Python module for remotely managing an OpenWRT instance via its Luci-exported JSONRPC interface.

See [the module specifications](spec.md) for information about the implemented functionality.

## Usage ##

Create a manager for a particular OpenWRT installation:
```python
>>> import openwrt
>>> manager = openwrt.create_manager(hostname='10.0.0.5', username='root', password='root')
```

### Managing forwarded ports ###
```python
# List all the forwarded ports
>>> port_forwarding_rules = manager.port_forwarding.all
>>> for rule in port_forwarding_rules:
>>>     print rule

# Modify a specific rule
>>> rule = port_forwarding_rules[1]
>>> updated_rule = rule.updated(dest_port=9080)
>>> manager.port_forwarding.update(updated_rule)

# Create a new rule
>>> from openwrt import PortForwardingRule
>>> new_rule = PortForwardingRule.create(name='My awesome forwarded port',
>>>     src='wan', src_dport=80, proto='tcp', dest='lan', dest_ip='192.168.1.10')
>>> manager.port_forwarding.add(new_rule)
```

*TODO: Usage of other manager services*

For more information, see `help(openwrt)`.
