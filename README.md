# OpenWRT JSONRPC client #

A client to OpenWRT's Luci-exported JSONRPC interface.

For more information about the JSONRPC interface, see:
http://luci.subsignal.org/trac/wiki/Documentation/JsonRpcHowTo

## Usage ##

Connection objects act as a direct proxy and can be used directly to call exported
methods on all the available libraries.

```python
import openwrt
client = openwrt.connect(openwrt_hostname='10.0.0.5', username='root', 'password'=root)
for path in client.fs.dir():
    print(path)
```

For more information, see `help(openwrt)`.
