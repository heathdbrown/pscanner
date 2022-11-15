# SPDX-FileCopyrightText: 2022-present Heath Brown <heathd.brown@gmail.com>
#
# SPDX-License-Identifier: MIT
import ipaddress
import socket
from typing import List
import sys

from colorama import init, Fore
from icmplib import async_multiping, ping, multiping


init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX


def are_alive(addresses: List[str]) -> List[str]:
    return [
        host.address for host in multiping(addresses, privileged=False) if host.is_alive
    ]


def is_host_alive(host: str) -> bool:
    if not ping(host, timeout=1, count=1, privileged=False).is_alive:
        print(f"{GRAY}{host:15} is not alive {RESET}")
        return False
    return True


def is_port_open(host: str, port: int) -> bool:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(3)
        try:
            sock.connect((host, int(port)))
        except ConnectionRefusedError:
            print(f"{GRAY}{host:15}:{port:5} is closed {RESET}")
            return False
        except TimeoutError:
            print(f"{GRAY}{host:15}:{port:5} timed out {RESET}")
            return False
        except KeyboardInterrupt:
            sys.exit()
        else:
            print(f"{GREEN}{host:15}:{port:5} is open {RESET}")
            return True


def is_subnet(ip: str) -> bool:
    return "/" in ip


def hosts_in_subnet(network: str) -> List[str]:
    if not is_subnet(network):
        print(f"{network} is not a network")

    return [str(host) for host in ipaddress.ip_network(network).hosts()]


def is_port_range(port: str) -> bool:
    if not port.find("-") == -1 or not port.find(",") == -1:
        return True

    return False


def split_port_with_comma(port: str) -> List[int]:
    return [int(_) for _ in port.split(",")]


def split_port_with_comma_str(port: str) -> List[str]:
    return [_ for _ in port.split(",")]


def split_port_with_dash(port: str) -> List[str]:
    return port.split("-")


def generate_port_range_from_dash(start_stop: List[str]) -> List[int]:
    return [_ for _ in range(int(start_stop[0]), int(start_stop[1]) + 1)]


def ports_from_range(port: str) -> List[int]:
    if "-" and not "," in port:
        return generate_port_range_from_dash(split_port_with_dash(port))

    if "," and not "-" in port:
        return split_port_with_comma(port)

    if "," and "-" in port:
        return [
            _
            for p in split_port_with_comma_str(port)
            for _ in generate_port_range_from_dash(split_port_with_dash(p))
        ]
