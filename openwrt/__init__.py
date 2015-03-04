

def create_rpc_proxy(hostname, username, password):
    """
    Creates and returns a proxy to OpenWRT's Luci-exported JSONRPC interface.

    For more information about the JSONRPC interface, see:
    http://luci.subsignal.org/trac/wiki/Documentation/JsonRpcHowTo

    Args:
        hostname: the hostname to the OpenWRT instance
        username: the configured Luci username
        password: the configured luci password

    Raises:
        rpcproxy.AuthenticationError: any call to an exported method can raise this when authentication fails

    Usage:
        Resulting connection objects act as a direct proxy and can be used directly to call exported
        methods on all the available libraries.

        >>> import openwrt
        >>> proxy = openwrt.create_rpc_proxy(hostname='10.0.0.5', username='root', 'password'=root)
        >>> for path in proxy.fs.dir():
        >>>     print(path)
    """
    import rpcproxy
    return rpcproxy.create(hostname, username, password)