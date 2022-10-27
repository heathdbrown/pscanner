# SPDX-FileCopyrightText: 2022-present U.N. Owen <void@some.where>
#
# SPDX-License-Identifier: MIT
import ipaddress
import socket
from typing import List
from colorama import init, Fore

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

def is_port_open(host: str, port: int) -> bool:
    try:
        s = socket.socket()
        s.connect((host, int(port)))
    except ConnectionRefusedError:
        print(f"{GRAY}{host:15}:{port:15} is closed {RESET}", end='/r')
    except TimeoutError:
        print(f"{GRAY}{host:15}:{port:15} is not alive {RESET}", end='/r')
    else:
        print(f"{GREEN}{host:15}:{port:15} is open {RESET}", end='/r')
    finally:
        s.close()

def is_subnet(ip: str) -> bool:
    if '/' in ip:
        return True
    else:
        return False

def hosts_in_subnet(network: str) -> List:
    if not is_subnet:
        print(f"{network} is not a network")
    
    return list(ipaddress.ip_network(network).hosts())