import pscanner
import pytest


def test_is_port_open():
    pass


def test_is_subnet():
    assert pscanner.is_subnet("192.168.1.0") == False
    assert pscanner.is_subnet("192.168.0/24") == True


def test_hosts_in_subnet():
    assert len(pscanner.hosts_in_subnet("192.168.0.0/29")) == 6
