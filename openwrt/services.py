
EXIT_SUCCESS = 0


class ServicesManager:

    def __init__(self, shell):
        self._shell = shell

    def restart(self, name):
        """
        Restarts the specified service.
        """
        exit_code = self._shell.call('/etc/init.d/{} restart'.format(name))
        if exit_code != EXIT_SUCCESS:
            raise RuntimeError('Restarting the service {} failed'.format(name))