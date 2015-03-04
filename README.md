# OpenWRT Remote Manager #

A Python module for remotely managing an OpenWRT instance via its Luci-exported JSONRPC interface.

For more information about the JSONRPC interface, see:
http://luci.subsignal.org/trac/wiki/Documentation/JsonRpcHowTo

## Usage ##

To issue raw JSONRPC calls, create a proxy object and use it as such:

```python
import openwrt
proxy = openwrt.create_rpc_proxy(hostname='10.0.0.5', username='root', 'password'=root)
for path in proxy.fs.dir():
    print(path)
```

For more information, see `help(openwrt)`.
