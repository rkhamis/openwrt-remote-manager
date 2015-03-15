

class UserManager:
    """
    Manager of Unix users on an OpenWRT installation.
    """

    def __init__(self, shell, rpc_proxy):
        self._shell = shell
        self._rpc_proxy = rpc_proxy

    @property
    def user_names(self):
        """
        Returns a collection of user names
        """
        return self._shell.execute("cat /etc/shadow | cut -d: -f1").split()

    def create_user(self, username):
        user_line = '{}:$1$t0U3k41r$OGeCoqdpwY5EewVdKwSt.0:16499:0:99999:7:::'.format(username)
        assert self._shell.call('echo "{}" >> /etc/shadow'.format(user_line)) == 0, 'Failed to create a user'

    def delete_user(self, username):
        command = 'sed -i "/^{}:/d" /etc/shadow'.format(username)
        assert self._shell.call(command) == 0, 'Failed to delete user'

    def change_password(self, username, password):
        assert self._rpc_proxy.sys.user.setpasswd(username, password) == 0, 'Failed to change password'

    def check_password(self, username, password):
        """
        Returns True if the given password checks out for the given username.
        """
        return self._rpc_proxy.sys.user.checkpasswd(username, password)