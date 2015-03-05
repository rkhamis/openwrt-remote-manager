
class Shell:
    """
    Executor of shell commands on OpenWRT instances via an RPC Proxy
    """

    def __init__(self, rpc_proxy):
        self._rpc = rpc_proxy

    def execute(self, command):
        """
        Executes a shell command and captures its standard output and returns it as a str.
        """
        return getattr(self._rpc.sys, 'exec')(command)

    def call(self, command):
        """
        Executes a shell command and returns its exist code.
        """
        return self._rpc.sys.call(command)