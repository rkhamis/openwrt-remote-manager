
from fixtures import *
import socket


def _http_head(hostname, port, url='/'):
    """
    Test if HTTP fails HEAD.
    """
    from httplib import HTTPConnection
    HTTPConnection(hostname, port).request('HEAD', url)


def test_clearing_all_installed_port_forwarding_rules():
    for rule in manager.port_forwarding.all:
        manager.port_forwarding.delete(rule)
    assert not manager.port_forwarding.all, 'A fresh installation should have no forwardings set up'


def test_creating_and_modifying_a_forwarded_port():
    from openwrt import PortForwardingRule

    # I'll forward the Luci port on OpenWRT to a different port
    FORWARDED_PORT = 80
    FORWARDED_TO_PORT = 9235
    FORWARDED_TO_PORT_2 = 9544

    # First make sure it's not forwarded
    with pytest.raises(socket.error) as _:
        _http_head(HOSTNAME, FORWARDED_TO_PORT)
        _http_head(HOSTNAME, FORWARDED_TO_PORT_2)

    new_rule = PortForwardingRule.create('New Luci port', src='lan', dest='lan',
                                         src_dport=FORWARDED_TO_PORT, dest_port=FORWARDED_PORT)
    manager.port_forwarding.add(new_rule)

    assert len(manager.port_forwarding.all) == 1

    # Now a connection to that forwarded port should be doable
    _http_head(HOSTNAME, FORWARDED_TO_PORT)

    # Now update the port forwarding to the second port
    updated_rule = manager.port_forwarding.all[0].updated(src_dport=FORWARDED_TO_PORT_2)
    manager.port_forwarding.update(updated_rule)

    # Test the old port stopped working
    with pytest.raises(socket.error) as _:
        _http_head(HOSTNAME, FORWARDED_TO_PORT)

    # and the new port is now listening
    _http_head(HOSTNAME, FORWARDED_TO_PORT_2)

    # Now delete the updated rule
    manager.port_forwarding.delete(updated_rule)

    assert not manager.port_forwarding.all
