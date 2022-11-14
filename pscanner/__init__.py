# SPDX-FileCopyrightText: 2022-present Heath Brown <heathd.brown@gmail.com>
#
# SPDX-License-Identifier: MIT
import ipaddress
import socket
from typing import List

from colorama import init, Fore
from icmplib import async_multiping, ping, multiping


init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX


def are_alive(addresses: List[str]) -> List[str]:
    return [host.address for host in multiping(addresses, privileged=False) if host.is_alive]


def is_host_alive(host: str) -> bool:
    if not ping(host, timeout=1, count=1, privileged=False).is_alive:
        print(f"{GRAY}{host:15} is not alive {RESET}")
        return False
    return True


def is_port_open(host: str, port: int) -> bool:
    try:
        s = socket.socket()
        s.connect((host, int(port)))
    except ConnectionRefusedError:
        print(f"{GRAY}{host:15}:{port:5} is closed {RESET}")
    except TimeoutError:
        print(f"{GRAY}{host:15}:{port:5} is not alive {RESET}")
    else:
        print(f"{GREEN}{host:15}:{port:5} is open {RESET}")
    finally:
        s.close()


def is_subnet(ip: str) -> bool:
    return "/" in ip


def hosts_in_subnet(network: str) -> List[str]:
    if not is_subnet(network):
        print(f"{network} is not a network")

    return [str(host) for host in ipaddress.ip_network(network).hosts()]
