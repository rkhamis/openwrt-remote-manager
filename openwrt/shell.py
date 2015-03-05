
class ShellManager:

    def __init__(self, rpc):
        self._rpc = rpc

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