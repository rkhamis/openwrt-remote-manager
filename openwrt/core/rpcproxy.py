from urllib2 import HTTPError
from jsonrpc_requests import Server


class Proxy:
    """
    An RPC proxy to an OpenWRT's Luci-exported JSONRPC interface.

    Call methods on this object qualified by their library name as if they are members of this object, for example;
    >>> proxy.fs.dir('/etc')
    would call the method `dir('/etc')` exported by the `fs` library.

    See http://luci.subsignal.org/trac/wiki/Documentation/JsonRpcHowTo for more documentation on the exported librabries
    and methods.
    """

    def __init__(self, hostname, username, password):
        self._hostname = hostname
        self._auth_username = username
        self._auth_password = password
        self._auth_token = None

    def http_url(self, library):
        url = "http://{}/cgi-bin/luci/rpc/{}".format(self._hostname, library)
        if self._auth_token:
            url += "?auth=" + self._auth_token
        return url

    def authenticate(self):
        """
        Authenticates this proxy and mutates its internal state according to the authentication result.
        """
        if not self._auth_token:
            self._auth_token = _json_rpc_call(self.http_url('auth'), 'login', self._auth_username, self._auth_password)

    def __getattr__(self, library_name):
        return _LibraryOrMethod(self, library_name)

    @property
    def hostname(self):
        return self._hostname


class AuthenticationError:

    def __init__(self, hostname):
        self._hostname = hostname

    def __str__(self):
        return "Failed to authenticate with OpenWRT at {}".format(self._hostname)


class _LibraryOrMethod:

    def __init__(self, proxy, name):
        self._proxy = proxy
        self._name = name

    def __getattr__(self, suffix_name):
        return _LibraryOrMethod(self._proxy, '{}.{}'.format(self._name, suffix_name))

    def __call__(self, *args, **kwargs):
        self._proxy.authenticate()
        name_components = self._name.split('.')
        library, method = name_components[0], '.'.join(name_components[1:])
        try:
            return _json_rpc_call(self._proxy.http_url(library), method, *args, **kwargs)
        except HTTPError as e:
            if e.code == 403:
                raise AuthenticationError(self.client.hostname)
            else:
                raise


def _json_rpc_call(url, method, *args, **kwargs):
    return getattr(Server(url), method).__call__(*args, **kwargs)