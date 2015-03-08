
import openwrt
import pytest
from openwrt import PortForwardingRule

"""
    Testing assumes there's an OpenWRT instance accessible at 10.0.0.5 and can be accessed via the username
    and password 'root' and 'root', and a network information called 'lan'.
"""
HOSTNAME = '10.0.0.5'
AUTH_USERNAME = 'root'
AUTH_PASSWORD = 'root'
manager = openwrt.create_manager(HOSTNAME, AUTH_USERNAME, AUTH_PASSWORD)