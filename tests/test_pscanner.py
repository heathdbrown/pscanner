import pscanner
import pytest


def test_is_port_open():
    pass


def test_is_subnet():
    assert pscanner.is_subnet("192.168.1.0") is False
    assert pscanner.is_subnet("192.168.0/24") is True


def test_hosts_in_subnet():
    assert len(pscanner.hosts_in_subnet("192.168.0.0/29")) == 6


def test_is_port_range():
    assert pscanner.is_port_range('22') is False
    assert pscanner.is_port_range("22-23") is True
    assert pscanner.is_port_range("22,23") is True
    assert pscanner.is_port_range("22-23,26-28") is True


def test_ports_from_range():
    assert pscanner.ports_from_range("22-23") == [22, 23]
    assert pscanner.ports_from_range("22,23") == [22, 23]
    assert pscanner.ports_from_range("80-83") == [80, 81, 82, 83]
    assert pscanner.ports_from_range("22-23,27-28") == [22, 23, 27, 28]
    assert pscanner.ports_from_range("80-83,90-93") == [80, 81, 82, 83, 90, 91, 92, 93]
