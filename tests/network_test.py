
from fixtures import *
from openwrt.network import StaticNetworkProfile, DHCPNetworkProfile


def test_network_devices():
    assert set(manager.network.devices) == {'lo', 'eth0'}


def test_network_profiles():
    profiles = manager.network.profiles

    assert len(profiles) == 2
    loopback = tuple(profile for profile in profiles if profile.interface_name == 'lo')[0]
    lan = tuple(profile for profile in profiles if profile.interface_name == 'eth0')[0]

    assert loopback.name == 'loopback'
    assert loopback.ip4_address == '127.0.0.1'
    assert isinstance(loopback, StaticNetworkProfile)

    assert lan.ip4_address == '10.0.0.5'
    assert lan.ip4_gateway == '10.0.0.1'


def test_adding_network_profile():
    profile = DHCPNetworkProfile('wireless', 'wlan0')
    manager.network.set_profile(profile)

    assert (p for p in manager.network.profiles if p.name == 'wireless')

    manager.network.delete_profile(profile)


def test_pinging():
    assert manager.network.ping_host('8.8.8.8')
