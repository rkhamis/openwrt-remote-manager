from urllib2 import HTTPError
from pyjsonrpc import HttpClient


class _Proxy:
    """
    An RPC proxy to an OpenWRT's Luci-exported JSONRPC interface.

    Call methods on this object qualified by their library name as if they are members of this object, for example;
    >>> proxy.fs.dir('/etc')
    would call the method `dir('/etc')` exported by the `fs` library.

    See http://luci.subsignal.org/trac/wiki/Documentation/JsonRpcHowTo for more documentation on the exported librabries
    and methods.
    """

    def __init__(self, openwrt_hostname, username, password):
        self._openwrt_hostname = openwrt_hostname
        self._auth_username = username
        self._auth_password = password
        self._auth_token = None

    def http_url(self, library):
        url = "http://{}/cgi-bin/luci/rpc/{}".format(self._openwrt_hostname, library)
        if self._auth_token:
            url += "?auth=" + self._auth_token
        return url

    def authenticate(self):
        """
        Authenticates this proxy and mutates its internal state according to the authentication result.
        """
        if not self._auth_token:
            self._auth_token = HttpClient(url=self.http_url('auth')).login(self._auth_username, self._auth_password)

    def __getattr__(self, library_name):
        return _Library(self, library_name)

    @property
    def hostname(self):
        return self._openwrt_hostname


class AuthenticationError:

    def __init__(self, hostname):
        self._hostname = hostname

    def __str__(self):
        return "Failed to authenticate with OpenWRT at {}".format(self._hostname)


class _Library:

    def __init__(self, client, library_name):
        self._client = client
        self._name = library_name

    @property
    def name(self):
        return self._name

    @property
    def client(self):
        return self._client

    @property
    def http_url(self):
        return self._client.http_url(self._name)

    def __getattr__(self, method_name):
        return _Method(self, method_name)


class _Method:

    def __init__(self, library, method_name):
        self._library = library
        self._name = method_name

    def __call__(self, *args, **kwargs):
        self._library.client.authenticate()
        try:
            return HttpClient(url=self._library.http_url).__call__(self._name, *args, **kwargs)
        except HTTPError as e:
            if e.code == 403:
                raise AuthenticationError(self._library.client.hostname)


def create(openwrt_hostname, username, password):
    return _Proxy(openwrt_hostname, username, password)
