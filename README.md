# OpenWRT Remote Manager #

A Python module for remotely managing an OpenWRT instance via its Luci-exported JSONRPC interface.

For more information about the JSONRPC interface, see:
http://luci.subsignal.org/trac/wiki/Documentation/JsonRpcHowTo

## Usage ##

Create a manager for a particular OpenWRT installation:
```python
import openwrt
manager = openwrt.create_manager(hostname='10.0.0.5', username='root', password='root')
```

### Managing forwarded ports ###
```python
# List all the forwarded ports
port_forwarding_rules = manager.port_forwarding.all
for rule in port_forwarding_rules:
    print rule

# Modify a specific rule
rule = port_forwarding_rules[1]
updated_rule = rule.updated(dest_port=9080)
manager.port_forwarding.update(updated_rule)

# Create a new rule
        option src       wan
        option src_dport 80
        option proto     tcp
        option dest      lan
        option dest_ip   192.168.1.10
from openwrt import PortForwardingRule
new_rule = PortForwardingRule.create(name='My awesome forwarded port',
    src='wan', src_dport=80, proto='tcp', dest='lan', dest_ip='192.168.1.10')
manager.port_forwarding.add(new_rule)
```

To issue raw JSONRPC calls, use the `rpc` attribute of the manager. Its attributes can be used as exported
JSONRPC libraries and their member attributes can be used as exported methods.

The exported JSONRPC libraries and their functions are documented here (don't mind the part about authentication though,
as the proxy object does that on-the-fly for you):
http://luci.subsignal.org/trac/wiki/Documentation/JsonRpcHowTo

```python
for path in manager.rpc.fs.dir('/etc'):
    print(path)
```

For more information, see `help(openwrt)`.
